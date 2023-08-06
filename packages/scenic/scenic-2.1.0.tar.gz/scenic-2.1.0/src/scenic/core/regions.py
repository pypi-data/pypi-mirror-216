"""Objects representing regions in space.

Manipulations of polygons and line segments are done using the
`shapely <https://github.com/shapely/shapely>`_ package.
"""

import math
import random
import itertools

import numpy
import shapely.geometry
import shapely.ops
import shapely.prepared

from scenic.core.distributions import (Samplable, RejectionException, needsSampling,
                                       distributionMethod)
from scenic.core.lazy_eval import valueInContext
from scenic.core.vectors import Vector, OrientedVector, VectorDistribution, VectorField
from scenic.core.geometry import _RotatedRectangle
from scenic.core.geometry import sin, cos, hypot, findMinMax, pointIsInCone, averageVectors
from scenic.core.geometry import headingOfSegment, triangulatePolygon, plotPolygon, polygonUnion
from scenic.core.type_support import toVector, toScalar
from scenic.core.utils import cached, cached_property

def toPolygon(thing):
	if needsSampling(thing):
		return None
	if hasattr(thing, 'polygon'):
		return thing.polygon
	if hasattr(thing, 'polygons'):
		return thing.polygons
	if hasattr(thing, 'lineString'):
		return thing.lineString
	return None

def regionFromShapelyObject(obj, orientation=None):
	"""Build a `Region` from Shapely geometry."""
	assert obj.is_valid, obj
	if obj.is_empty:
		return nowhere
	elif isinstance(obj, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)):
		return PolygonalRegion(polygon=obj, orientation=orientation)
	elif isinstance(obj, (shapely.geometry.LineString, shapely.geometry.MultiLineString)):
		return PolylineRegion(polyline=obj, orientation=orientation)
	elif isinstance(obj, shapely.geometry.MultiPoint):
		points = [pt.coords[0] for pt in obj.geoms]
		return PointSetRegion('PointSet', points, orientation=orientation)
	elif isinstance(obj, shapely.geometry.Point):
		return PointSetRegion('PointSet', obj.coords, orientation=orientation)
	else:
		raise TypeError(f'unhandled type of Shapely geometry: {obj}')

def orientationFor(first, second, reversed):
	o1 = first.orientation
	o2 = second.orientation
	if reversed:
		o1, o2 = o2, o1
	if not o1:
		o1 = o2
	return o1

class PointInRegionDistribution(VectorDistribution):
	"""Uniform distribution over points in a Region."""
	def __init__(self, region):
		super().__init__(region)
		self.region = region

	def sampleGiven(self, value):
		return value[self.region].uniformPointInner()

	@property
	def heading(self):
		if self.region.orientation is not None:
			return self.region.orientation[self]
		else:
			return 0

	def __repr__(self):
		return f'PointIn({self.region!r})'

class Region(Samplable):
	"""Abstract class for regions."""
	def __init__(self, name, *dependencies, orientation=None):
		super().__init__(dependencies)
		self.name = name
		self.orientation = orientation

	def sampleGiven(self, value):
		return self

	def intersect(self, other, triedReversed=False) -> 'Region':
		"""intersect(other)

		Get a `Region` representing the intersection of this one with another.

		If both regions have a :term:`preferred orientation`, the one of ``self``
		is inherited by the intersection.
		"""
		if triedReversed:
			orientation = orientationFor(self, other, triedReversed)
			return IntersectionRegion(self, other, orientation=orientation)
		else:
			return other.intersect(self, triedReversed=True)

	def intersects(self, other, triedReversed=False) -> bool:
		"""intersects(other)

		Check if this `Region` intersects another.
		"""
		if triedReversed:
			# Last-ditch attempt to check intersection by converting to polygons
			p1, p2 = toPolygon(self), toPolygon(other)
			if p1 is not None and p2 is not None:
				return not (p1 & p2).is_empty
			raise NotImplementedError
		else:
			return other.intersects(self, triedReversed=True)

	def difference(self, other) -> 'Region':
		"""Get a `Region` representing the difference of this one and another."""
		if isinstance(other, EmptyRegion):
			return self
		elif isinstance(other, AllRegion):
			return nowhere
		return DifferenceRegion(self, other)

	def union(self, other, triedReversed=False) -> 'Region':
		"""union(other)

		Get a `Region` representing the union of this one with another.

		Not supported by all region types.
		"""
		if triedReversed:
			raise NotImplementedError
		else:
			return other.union(self, triedReversed=True)

	@staticmethod
	def uniformPointIn(region):
		"""Get a uniform `Distribution` over points in a `Region`."""
		return PointInRegionDistribution(region)

	def uniformPointInner(self):
		"""Do the actual random sampling. Implemented by subclasses."""
		raise NotImplementedError

	def containsPoint(self, point) -> bool:
		"""Check if the `Region` contains a point. Implemented by subclasses."""
		raise NotImplementedError

	def containsObject(self, obj) -> bool:
		"""Check if the `Region` contains an `Object`.

		The default implementation assumes the `Region` is convex; subclasses must
		override the method if this is not the case.
		"""
		for corner in obj.corners:
			if not self.containsPoint(corner):
				return False
		return True

	def __contains__(self, thing) -> bool:
		"""Check if this `Region` contains an object or vector."""
		from scenic.core.object_types import Object
		if isinstance(thing, Object):
			return self.containsObject(thing)
		vec = toVector(thing, '"X in Y" with X not an Object or a vector')
		return self.containsPoint(vec)

	@distributionMethod
	def distanceTo(self, point) -> float:
		"""Distance to this region from a given point.

		Not supported by all region types.
		"""
		# Last-ditch attempt to compute distance by converting to polygon
		poly = toPolygon(self)
		if poly is not None:
			return poly.distance(shapely.geometry.Point(point))
		raise NotImplementedError

	def getAABB(self):
		"""Axis-aligned bounding box for this `Region`. Implemented by some subclasses."""
		raise NotImplementedError

	def orient(self, vec):
		"""Orient the given vector along the region's orientation, if any."""
		if self.orientation is None:
			return vec
		else:
			return OrientedVector(vec.x, vec.y, self.orientation[vec])

	def __str__(self):
		s = f'<{type(self).__name__}'
		if self.name:
			s += f' {self.name}'
		return s + '>'

	def __repr__(self):
		s = f'<{type(self).__name__}'
		if self.name:
			s += f' {self.name}'
		return s + f' at {hex(id(self))}>'

class AllRegion(Region):
	"""Region consisting of all space."""
	def intersect(self, other, triedReversed=False):
		return other

	def intersects(self, other, triedReversed=False):
		return not isinstance(other, EmptyRegion)

	def union(self, other, triedReversed=False):
		return self

	def containsPoint(self, point):
		return True

	def containsObject(self, obj):
		return True

	def containsRegion(self, reg, tolerance=0):
		return True

	def distanceTo(self, point):
		return 0

	def __eq__(self, other):
		return type(other) is AllRegion

	def __hash__(self):
		return hash(AllRegion)

class EmptyRegion(Region):
	"""Region containing no points."""
	def intersect(self, other, triedReversed=False):
		return self

	def intersects(self, other, triedReversed=False):
		return False

	def difference(self, other):
		return self

	def union(self, other, triedReversed=False):
		return other

	def uniformPointInner(self):
		raise RejectionException(f'sampling empty Region')

	def containsPoint(self, point):
		return False

	def containsObject(self, obj):
		return False

	def containsRegion(self, reg, tolerance=0):
		return type(reg) is EmptyRegion

	def distanceTo(self, point):
		return float('inf')

	def show(self, plt, style=None, **kwargs):
		pass

	def __eq__(self, other):
		return type(other) is EmptyRegion

	def __hash__(self):
		return hash(EmptyRegion)

#: A `Region` containing all points.
#:
#: Points may not be sampled from this region, as no uniform distribution over it exists.
everywhere = AllRegion('everywhere')

#: A `Region` containing no points.
#:
#: Attempting to sample from this region causes the sample to be rejected.
nowhere = EmptyRegion('nowhere')

class CircularRegion(Region):
	"""A circular region with a possibly-random center and radius.

	Args:
		center (`Vector`): center of the disc.
		radius (float): radius of the disc.
		resolution (int; optional): number of vertices to use when approximating this region as a
			polygon.
		name (str; optional): name for debugging.
	"""
	def __init__(self, center, radius, resolution=32, name=None):
		super().__init__(name, center, radius)
		self.center = toVector(center, "center of CircularRegion not a vector")
		self.radius = toScalar(radius, "radius of CircularRegion not a scalar")
		self.circumcircle = (self.center, self.radius)
		self.resolution = resolution

	@cached_property
	def polygon(self):
		assert not (needsSampling(self.center) or needsSampling(self.radius))
		ctr = shapely.geometry.Point(self.center)
		return ctr.buffer(self.radius, resolution=self.resolution)

	def sampleGiven(self, value):
		return CircularRegion(value[self.center], value[self.radius],
		                      name=self.name, resolution=self.resolution)

	def evaluateInner(self, context):
		center = valueInContext(self.center, context)
		radius = valueInContext(self.radius, context)
		return CircularRegion(center, radius,
		                      name=self.name, resolution=self.resolution)

	def intersects(self, other, triedReversed=False):
		if isinstance(other, CircularRegion):
			return self.center.distanceTo(other.center) <= self.radius + other.radius
		return super().intersects(other, triedReversed)

	def containsPoint(self, point):
		point = point.toVector()
		return point.distanceTo(self.center) <= self.radius

	def distanceTo(self, point):
		return max(0, point.distanceTo(self.center) - self.radius)

	def uniformPointInner(self):
		x, y = self.center
		r = random.triangular(0, self.radius, self.radius)
		t = random.uniform(-math.pi, math.pi)
		pt = Vector(x + (r * cos(t)), y + (r * sin(t)))
		return self.orient(pt)

	def getAABB(self):
		x, y = self.center
		r = self.radius
		return ((x - r, y - r), (x + r, y + r))

	def __repr__(self):
		return f'CircularRegion({self.center!r}, {self.radius!r})'

class SectorRegion(Region):
	"""A sector of a `CircularRegion`.

	This region consists of a sector of a disc, i.e. the part of a disc subtended by a
	given arc.

	Args:
		center (`Vector`): center of the corresponding disc.
		radius (float): radius of the disc.
		heading (float): heading of the centerline of the sector.
		angle (float): angle subtended by the sector.
		resolution (int; optional): number of vertices to use when approximating this region as a
			polygon.
		name (str; optional): name for debugging.
	"""
	def __init__(self, center, radius, heading, angle, resolution=32, name=None):
		self.center = toVector(center, "center of SectorRegion not a vector")
		self.radius = toScalar(radius, "radius of SectorRegion not a scalar")
		self.heading = toScalar(heading, "heading of SectorRegion not a scalar")
		self.angle = toScalar(angle, "angle of SectorRegion not a scalar")
		super().__init__(name, self.center, radius, heading, angle)
		r = (radius / 2) * cos(angle / 2)
		self.circumcircle = (self.center.offsetRadially(r, heading), r)
		self.resolution = resolution

	@cached_property
	def polygon(self):
		center, radius = self.center, self.radius
		ctr = shapely.geometry.Point(center)
		circle = ctr.buffer(radius, resolution=self.resolution)
		if self.angle >= math.tau - 0.001:
			return circle
		else:
			heading = self.heading
			half_angle = self.angle / 2
			mask = shapely.geometry.Polygon([
			    center,
			    center.offsetRadially(radius, heading + half_angle),
			    center.offsetRadially(2*radius, heading),
			    center.offsetRadially(radius, heading - half_angle)
			])
			return circle & mask

	def sampleGiven(self, value):
		return SectorRegion(value[self.center], value[self.radius],
			value[self.heading], value[self.angle],
			name=self.name, resolution=self.resolution)

	def evaluateInner(self, context):
		center = valueInContext(self.center, context)
		radius = valueInContext(self.radius, context)
		heading = valueInContext(self.heading, context)
		angle = valueInContext(self.angle, context)
		return SectorRegion(center, radius, heading, angle,
		                    name=self.name, resolution=self.resolution)

	def containsPoint(self, point):
		point = point.toVector()
		if not pointIsInCone(tuple(point), tuple(self.center), self.heading, self.angle):
			return False
		return point.distanceTo(self.center) <= self.radius

	def uniformPointInner(self):
		x, y = self.center
		heading, angle, maxDist = self.heading, self.angle, self.radius
		r = random.triangular(0, maxDist, maxDist)
		ha = angle / 2.0
		t = random.uniform(-ha, ha) + (heading + (math.pi / 2))
		pt = Vector(x + (r * cos(t)), y + (r * sin(t)))
		return self.orient(pt)

	def __repr__(self):
		return (f'SectorRegion({self.center!r}, {self.radius!r}, '
		        f'{self.heading!r}, {self.angle!r})')

class RectangularRegion(_RotatedRectangle, Region):
	"""A rectangular region with a possibly-random position, heading, and size.

	Args:
		position (`Vector`): center of the rectangle.
		heading (float): the heading of the ``length`` axis of the rectangle.
		width (float): width of the rectangle.
		length (float): length of the rectangle.
		name (str; optional): name for debugging.
	"""
	def __init__(self, position, heading, width, length, name=None):
		super().__init__(name, position, heading, width, length)
		self.position = toVector(position, "position of RectangularRegion not a vector")
		self.heading = toScalar(heading, "heading of RectangularRegion not a scalar")
		self.width = toScalar(width, "width of RectangularRegion not a scalar")
		self.length = toScalar(length, "length of RectangularRegion not a scalar")
		self.hw = hw = width / 2
		self.hl = hl = length / 2
		self.radius = hypot(hw, hl)		# circumcircle; for collision detection
		self.corners = tuple(self.position.offsetRotated(heading, Vector(*offset))
			for offset in ((hw, hl), (-hw, hl), (-hw, -hl), (hw, -hl)))
		self.circumcircle = (self.position, self.radius)

	def sampleGiven(self, value):
		return RectangularRegion(value[self.position], value[self.heading],
			value[self.width], value[self.length],
			name=self.name)

	def evaluateInner(self, context):
		position = valueInContext(self.position, context)
		heading = valueInContext(self.heading, context)
		width = valueInContext(self.width, context)
		length = valueInContext(self.length, context)
		return RectangularRegion(position, heading, width, length,
		                         name=self.name)

	def uniformPointInner(self):
		hw, hl = self.hw, self.hl
		rx = random.uniform(-hw, hw)
		ry = random.uniform(-hl, hl)
		pt = self.position.offsetRotated(self.heading, Vector(rx, ry))
		return self.orient(pt)

	def getAABB(self):
		x, y = zip(*self.corners)
		minx, maxx = findMinMax(x)
		miny, maxy = findMinMax(y)
		return ((minx, miny), (maxx, maxy))

	def __repr__(self):
		return (f'RectangularRegion({self.position!r}, {self.heading!r}, '
		        f'{self.width!r}, {self.length!r})')

class PolylineRegion(Region):
	"""Region given by one or more polylines (chain of line segments).

	The region may be specified by giving either a sequence of points or ``shapely``
	polylines (a ``LineString`` or ``MultiLineString``).

	Args:
		points: sequence of points making up the polyline (or `None` if using the
			**polyline** argument instead).
		polyline: ``shapely`` polyline or collection of polylines (or `None` if using
			the **points** argument instead).
		orientation (optional): :term:`preferred orientation` to use, or `True` to use an
			orientation aligned with the direction of the polyline (the default).
		name (str; optional): name for debugging.
	"""
	def __init__(self, points=None, polyline=None, orientation=True, name=None):
		if orientation is True:
			orientation = VectorField('Polyline', self.defaultOrientation)
			self.usingDefaultOrientation = True
		else:
			self.usingDefaultOrientation = False
		super().__init__(name, orientation=orientation)
		if points is not None:
			points = tuple(points)
			if len(points) < 2:
				raise ValueError('tried to create PolylineRegion with < 2 points')
			self.points = points
			self.lineString = shapely.geometry.LineString(points)
		elif polyline is not None:
			if isinstance(polyline, shapely.geometry.LineString):
				if len(polyline.coords) < 2:
					raise ValueError('tried to create PolylineRegion with <2-point LineString')
			elif isinstance(polyline, shapely.geometry.MultiLineString):
				if len(polyline.geoms) == 0:
					raise ValueError('tried to create PolylineRegion from empty MultiLineString')
				for line in polyline.geoms:
					assert len(line.coords) >= 2
			else:
				raise ValueError('tried to create PolylineRegion from non-LineString')
			self.lineString = polyline
			self.points = None
		else:
			raise ValueError('must specify points or polyline for PolylineRegion')
		if not self.lineString.is_valid:
			raise ValueError('tried to create PolylineRegion with '
			                 f'invalid LineString {self.lineString}')
		self.segments = self.segmentsOf(self.lineString)
		cumulativeLengths = []
		total = 0
		for p, q in self.segments:
			dx, dy = p[0] - q[0], p[1] - q[1]
			total += math.hypot(dx, dy)
			cumulativeLengths.append(total)
		self.cumulativeLengths = cumulativeLengths
		if self.points is None:
			pts = []
			last = None
			for p, q in self.segments:
				if p != last:
					pts.append(p)
				pts.append(q)
				last = q
			self.points = tuple(pts)

	@classmethod
	def segmentsOf(cls, lineString):
		if isinstance(lineString, shapely.geometry.LineString):
			segments = []
			points = list(lineString.coords)
			if len(points) < 2:
				raise ValueError('LineString has fewer than 2 points')
			last = points[0][:2]
			for point in points[1:]:
				point = point[:2]
				segments.append((last, point))
				last = point
			return segments
		elif isinstance(lineString, shapely.geometry.MultiLineString):
			allSegments = []
			for line in lineString.geoms:
				allSegments.extend(cls.segmentsOf(line))
			return allSegments
		else:
			raise ValueError('called segmentsOf on non-linestring')

	@cached_property
	def start(self):
		"""Get an `OrientedPoint` at the start of the polyline.

		The OP's heading will be aligned with the orientation of the region, if
		there is one (the default orientation pointing along the polyline).
		"""
		pointA, pointB = self.segments[0]
		if self.usingDefaultOrientation:
			heading = headingOfSegment(pointA, pointB)
		elif self.orientation is not None:
			heading = self.orientation[Vector(*pointA)]
		else:
			heading = 0
		from scenic.core.object_types import OrientedPoint
		return OrientedPoint(position=pointA, heading=heading)

	@cached_property
	def end(self):
		"""Get an `OrientedPoint` at the end of the polyline.

		The OP's heading will be aligned with the orientation of the region, if
		there is one (the default orientation pointing along the polyline).
		"""
		pointA, pointB = self.segments[-1]
		if self.usingDefaultOrientation:
			heading = headingOfSegment(pointA, pointB)
		elif self.orientation is not None:
			heading = self.orientation[Vector(*pointB)]
		else:
			heading = 0
		from scenic.core.object_types import OrientedPoint
		return OrientedPoint(position=pointB, heading=heading)

	def defaultOrientation(self, point):
		start, end = self.nearestSegmentTo(point)
		return start.angleTo(end)

	def uniformPointInner(self):
		pointA, pointB = random.choices(self.segments,
		                                cum_weights=self.cumulativeLengths)[0]
		interpolation = random.random()
		x, y = averageVectors(pointA, pointB, weight=interpolation)
		if self.usingDefaultOrientation:
			return OrientedVector(x, y, headingOfSegment(pointA, pointB))
		else:
			return self.orient(Vector(x, y))

	def intersect(self, other, triedReversed=False):
		poly = toPolygon(other)
		if poly is not None:
			intersection = self.lineString & poly
			line_geoms = (shapely.geometry.LineString, shapely.geometry.MultiLineString)
			if (isinstance(intersection, shapely.geometry.GeometryCollection)
			    and intersection.length > 0):
				geoms = [geom for geom in intersection.geoms if isinstance(geom, line_geoms)]
				intersection = shapely.ops.unary_union(geoms)
			orientation = orientationFor(self, other, triedReversed)
			return regionFromShapelyObject(intersection, orientation=orientation)
		return super().intersect(other, triedReversed)

	def intersects(self, other, triedReversed=False):
		poly = toPolygon(other)
		if poly is not None:
			intersection = self.lineString & poly
			return not intersection.is_empty
		return super().intersects(other, triedReversed)

	def difference(self, other):
		poly = toPolygon(other)
		if poly is not None:
			diff = self.lineString - poly
			return regionFromShapelyObject(diff)
		return super().difference(other)

	@staticmethod
	def unionAll(regions):
		regions = tuple(regions)
		if not regions:
			return nowhere
		if any(not isinstance(region, PolylineRegion) for region in regions):
			raise TypeError(f'cannot take Polyline union of regions {regions}')
		# take union by collecting LineStrings, to preserve the order of points
		strings = []
		for region in regions:
			string = region.lineString
			if isinstance(string, shapely.geometry.MultiLineString):
				strings.extend(string.geoms)
			else:
				strings.append(string)
		newString = shapely.geometry.MultiLineString(strings)
		return PolylineRegion(polyline=newString)

	def containsPoint(self, point):
		return self.lineString.intersects(shapely.geometry.Point(point))

	def containsObject(self, obj):
		return False

	@distributionMethod
	def distanceTo(self, point) -> float:
		return self.lineString.distance(shapely.geometry.Point(point))

	@distributionMethod
	def signedDistanceTo(self, point) -> float:
		"""Compute the signed distance of the PolylineRegion to a point.

		The distance is positive if the point is left of the nearest segment,
		and negative otherwise.
		"""
		dist = self.distanceTo(point)
		start, end = self.nearestSegmentTo(point)
		rp = point - start
		tangent = end - start
		return dist if tangent.angleWith(rp) >= 0 else -dist

	@distributionMethod
	def project(self, point):
		pt = shapely.ops.nearest_points(self.lineString, shapely.geometry.Point(point))[0]
		return Vector(*pt.coords[0])

	@distributionMethod
	def nearestSegmentTo(self, point):
		dist = self.lineString.project(shapely.geometry.Point(point))
		# TODO optimize?
		for segment, cumLen in zip(self.segments, self.cumulativeLengths):
			if dist <= cumLen:
				break
		# FYI, could also get here if loop runs to completion due to rounding error
		return (Vector(*segment[0]), Vector(*segment[1]))

	def pointAlongBy(self, distance, normalized=False) -> Vector:
		"""Find the point a given distance along the polyline from its start.

		If **normalized** is true, then distance should be between 0 and 1, and
		is interpreted as a fraction of the length of the polyline. So for example
		``pointAlongBy(0.5, normalized=True)`` returns the polyline's midpoint.
		"""
		pt = self.lineString.interpolate(distance, normalized=normalized)
		return Vector(pt.x, pt.y)

	def equallySpacedPoints(self, num):
		return [self.pointAlongBy(d) for d in numpy.linspace(0, self.length, num)]

	def pointsSeparatedBy(self, distance):
		return [self.pointAlongBy(d) for d in numpy.arange(0, self.length, distance)]

	@property
	def length(self):
		return self.lineString.length

	def getAABB(self):
		xmin, ymin, xmax, ymax = self.lineString.bounds
		return ((xmin, ymin), (xmax, ymax))

	def show(self, plt, style='r-', **kwargs):
		plotPolygon(self.lineString, plt, style=style, **kwargs)

	def __getitem__(self, i) -> Vector:
		"""Get the ith point along this polyline.

		If the region consists of multiple polylines, this order is linear
		along each polyline but arbitrary across different polylines.
		"""
		return Vector(*self.points[i])

	def __add__(self, other):
		if not isinstance(other, PolylineRegion):
			return NotImplemented
		# take union by collecting LineStrings, to preserve the order of points
		strings = []
		for region in (self, other):
			string = region.lineString
			if isinstance(string, shapely.geometry.MultiLineString):
				strings.extend(string.geoms)
			else:
				strings.append(string)
		newString = shapely.geometry.MultiLineString(strings)
		return PolylineRegion(polyline=newString)

	def __len__(self) -> int:
		"""Get the number of vertices of the polyline."""
		return len(self.points)

	def __repr__(self):
		return f'PolylineRegion({self.lineString!r})'

	def __eq__(self, other):
		if type(other) is not PolylineRegion:
			return NotImplemented
		return (other.lineString == self.lineString)

	@cached
	def __hash__(self):
		return hash(str(self.lineString))

class PolygonalRegion(Region):
	"""Region given by one or more polygons (possibly with holes).

	The region may be specified by giving either a sequence of points defining the
	boundary of the polygon, or a collection of ``shapely`` polygons (a ``Polygon``
	or ``MultiPolygon``).

	Args:
		points: sequence of points making up the boundary of the polygon (or `None` if
			using the **polygon** argument instead).
		polygon: ``shapely`` polygon or collection of polygons (or `None` if using
			the **points** argument instead).
		orientation (`VectorField`; optional): :term:`preferred orientation` to use.
		name (str; optional): name for debugging.
	"""
	def __init__(self, points=None, polygon=None, orientation=None, name=None):
		super().__init__(name, orientation=orientation)
		if polygon is None and points is None:
			raise ValueError('must specify points or polygon for PolygonalRegion')
		if polygon is None:
			points = tuple(points)
			if len(points) == 0:
				raise ValueError('tried to create PolygonalRegion from empty point list!')
			for point in points:
				if needsSampling(point):
					raise ValueError('only fixed PolygonalRegions are supported')
			self.points = points
			polygon = shapely.geometry.Polygon(points)

		if isinstance(polygon, shapely.geometry.Polygon):
			self.polygons = shapely.geometry.MultiPolygon([polygon])
		elif isinstance(polygon, shapely.geometry.MultiPolygon):
			self.polygons = polygon
		else:
			raise ValueError(f'tried to create PolygonalRegion from non-polygon {polygon}')
		if not self.polygons.is_valid:
			raise ValueError('tried to create PolygonalRegion with '
			                 f'invalid polygon {self.polygons}')

		if (points is None and len(self.polygons.geoms) == 1
		    and len(self.polygons.geoms[0].interiors) == 0):
			self.points = tuple(self.polygons.geoms[0].exterior.coords[:-1])

		if self.polygons.is_empty:
			raise ValueError('tried to create empty PolygonalRegion')

		triangles = []
		for polygon in self.polygons.geoms:
			triangles.extend(triangulatePolygon(polygon))
		assert len(triangles) > 0, self.polygons
		self.trianglesAndBounds = tuple((tri, tri.bounds) for tri in triangles)
		areas = (triangle.area for triangle in triangles)
		self.cumulativeTriangleAreas = tuple(itertools.accumulate(areas))

	def uniformPointInner(self):
		triangle, bounds = random.choices(
			self.trianglesAndBounds,
			cum_weights=self.cumulativeTriangleAreas)[0]
		minx, miny, maxx, maxy = bounds
		# TODO improve?
		while True:
			x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
			if triangle.intersects(shapely.geometry.Point(x, y)):
				return self.orient(Vector(x, y))

	def difference(self, other):
		poly = toPolygon(other)
		if poly is not None:
			diff = self.polygons - poly
			return regionFromShapelyObject(diff, orientation=self.orientation)
		return super().difference(other)

	def intersect(self, other, triedReversed=False):
		poly = toPolygon(other)
		if poly is not None:
			intersection = self.polygons & poly
			if isinstance(intersection, shapely.geometry.GeometryCollection):
				if intersection.area > 0:
					poly_geoms = (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)
					geoms = [geom for geom in intersection.geoms if isinstance(geom, poly_geoms)]
				elif intersection.length > 0:
					line_geoms = (shapely.geometry.LineString, shapely.geometry.MultiLineString)
					geoms = [geom for geom in intersection.geoms if isinstance(geom, line_geoms)]
				intersection = shapely.ops.unary_union(geoms)
			orientation = orientationFor(self, other, triedReversed)
			return regionFromShapelyObject(intersection, orientation=orientation)
		return super().intersect(other, triedReversed)

	def intersects(self, other, triedReversed=False):
		poly = toPolygon(other)
		if poly is not None:
			intersection = self.polygons & poly
			return not intersection.is_empty
		return super().intersects(other, triedReversed)

	def union(self, other, triedReversed=False, buf=0):
		poly = toPolygon(other)
		if not poly:
			return super().union(other, triedReversed)
		union = polygonUnion((self.polygons, poly), buf=buf)
		orientation = VectorField.forUnionOf((self, other), tolerance=buf)
		return PolygonalRegion(polygon=union, orientation=orientation)

	@staticmethod
	def unionAll(regions, buf=0):
		regs, polys = [], []
		for reg in regions:
			if reg != nowhere:
				regs.append(reg)
				polys.append(toPolygon(reg))
		if not polys:
			return nowhere
		if any(not poly for poly in polys):
			raise TypeError(f'cannot take union of regions {regions}')
		union = polygonUnion(polys, buf=buf)
		orientation = VectorField.forUnionOf(regs, tolerance=buf)
		return PolygonalRegion(polygon=union, orientation=orientation)

	@property
	def boundary(self) -> PolylineRegion:
		"""Get the boundary of this region as a `PolylineRegion`."""
		return PolylineRegion(polyline=self.polygons.boundary)

	def buffer(self, distance):
		return PolygonalRegion(polygon=self.polygons.buffer(distance))

	@cached_property
	def prepared(self):
		return shapely.prepared.prep(self.polygons)

	def containsPoint(self, point):
		return self.prepared.intersects(shapely.geometry.Point(point))

	def containsObject(self, obj):
		objPoly = obj.polygon
		if objPoly is None:
			raise ValueError('tried to test containment of symbolic Object!')
		# TODO improve boundary handling?
		return self.prepared.contains(objPoly)

	def containsRegion(self, other, tolerance=0):
		if isinstance(other, EmptyRegion):
			return True
		poly = toPolygon(other)
		if poly is None:
			raise TypeError(f'cannot test inclusion of {other} in PolygonalRegion')
		return self.polygons.buffer(tolerance).contains(poly)

	@distributionMethod
	def distanceTo(self, point):
		return self.polygons.distance(shapely.geometry.Point(point))

	def getAABB(self):
		xmin, ymin, xmax, ymax = self.polygons.bounds
		return ((xmin, ymin), (xmax, ymax))

	def show(self, plt, style='r-', **kwargs):
		plotPolygon(self.polygons, plt, style=style, **kwargs)

	def __repr__(self):
		return f'PolygonalRegion({self.polygons!r})'

	def __eq__(self, other):
		if type(other) is not PolygonalRegion:
			return NotImplemented
		return (other.polygons == self.polygons
		        and other.orientation == self.orientation)

	@cached
	def __hash__(self):
		# TODO better way to hash mutable Shapely geometries? (also for PolylineRegion)
		return hash((str(self.polygons), self.orientation))

	def __getstate__(self):
		state = self.__dict__.copy()
		state.pop('_cached_prepared', None)		# prepared geometries are not picklable
		return state

class PointSetRegion(Region):
	"""Region consisting of a set of discrete points.

	No `Object` can be contained in a `PointSetRegion`, since the latter is discrete.
	(This may not be true for subclasses, e.g. `GridRegion`.)

	Args:
		name (str): name for debugging
		points (arraylike): set of points comprising the region
		kdTree (`scipy.spatial.KDTree`, optional): k-D tree for the points (one will
		  be computed if none is provided)
		orientation (`VectorField`; optional): :term:`preferred orientation` for the
			region
		tolerance (float; optional): distance tolerance for checking whether a point lies
		  in the region
	"""

	def __init__(self, name, points, kdTree=None, orientation=None, tolerance=1e-6):
		super().__init__(name, orientation=orientation)
		self.points = numpy.array(points)
		for point in self.points:
			if needsSampling(point):
				raise ValueError('only fixed PointSetRegions are supported')
		import scipy.spatial	# slow import not often needed
		self.kdTree = scipy.spatial.KDTree(self.points) if kdTree is None else kdTree
		self.orientation = orientation
		self.tolerance = tolerance

	def uniformPointInner(self):
		i = random.randrange(0, len(self.points))
		return self.orient(Vector(*self.points[i]))

	def intersect(self, other, triedReversed=False):
		def sampler(intRegion):
			o = intRegion.regions[1]
			center, radius = o.circumcircle
			possibles = (Vector(*self.kdTree.data[i])
			             for i in self.kdTree.query_ball_point(center, radius))
			intersection = [p for p in possibles if o.containsPoint(p)]
			if len(intersection) == 0:
				raise RejectionException(f'empty intersection of Regions {self} and {o}')
			return self.orient(random.choice(intersection))
		orientation = orientationFor(self, other, triedReversed)
		return IntersectionRegion(self, other, sampler=sampler, orientation=orientation)

	def containsPoint(self, point):
		distance, location = self.kdTree.query(point)
		return (distance <= self.tolerance)

	def containsObject(self, obj):
		return False

	@distributionMethod
	def distanceTo(self, point):
		distance, _ = self.kdTree.query(point)
		return distance

	def __eq__(self, other):
		if type(other) is not PointSetRegion:
			return NotImplemented
		return (self.name == other.name
		        and numpy.array_equal(self.points, other.points)
		        and self.orientation == other.orientation)

	@cached
	def __hash__(self):
		return hash((self.name, self.points.tobytes(), self.orientation))

class GridRegion(PointSetRegion):
	"""A Region given by an obstacle grid.

	A point is considered to be in a `GridRegion` if the nearest grid point is
	not an obstacle.

	Args:
		name (str): name for debugging
		grid: 2D list, tuple, or NumPy array of 0s and 1s, where 1 indicates an obstacle
		  and 0 indicates free space
		Ax (float): spacing between grid points along X axis
		Ay (float): spacing between grid points along Y axis
		Bx (float): X coordinate of leftmost grid column
		By (float): Y coordinate of lowest grid row
		orientation (`VectorField`; optional): orientation of region
	"""
	def __init__(self, name, grid, Ax, Ay, Bx, By, orientation=None):
		self.grid = numpy.array(grid)
		self.sizeY, self.sizeX = self.grid.shape
		self.Ax, self.Ay = Ax, Ay
		self.Bx, self.By = Bx, By
		y, x = numpy.where(self.grid == 0)
		points = [self.gridToPoint(point) for point in zip(x, y)]
		super().__init__(name, points, orientation=orientation)

	def gridToPoint(self, gp):
		x, y = gp
		return ((self.Ax * x) + self.Bx, (self.Ay * y) + self.By)

	def pointToGrid(self, point):
		x, y = point
		x = (x - self.Bx) / self.Ax
		y = (y - self.By) / self.Ay
		nx = int(round(x))
		if nx < 0 or nx >= self.sizeX:
			return None
		ny = int(round(y))
		if ny < 0 or ny >= self.sizeY:
			return None
		return (nx, ny)

	def containsPoint(self, point):
		gp = self.pointToGrid(point)
		if gp is None:
			return False
		x, y = gp
		return (self.grid[y, x] == 0)

	def containsObject(self, obj):
		# TODO improve this procedure!
		# Fast check
		for c in obj.corners:
			if not self.containsPoint(c):
				return False
		# Slow check
		gps = [self.pointToGrid(corner) for corner in obj.corners]
		x, y = zip(*gps)
		minx, maxx = findMinMax(x)
		miny, maxy = findMinMax(y)
		for x in range(minx, maxx+1):
			for y in range(miny, maxy+1):
				p = self.gridToPoint((x, y))
				if self.grid[y, x] == 1 and obj.containsPoint(p):
					return False
		return True

class IntersectionRegion(Region):
	def __init__(self, *regions, orientation=None, sampler=None, name=None):
		self.regions = tuple(regions)
		if len(self.regions) < 2:
			raise ValueError('tried to take intersection of fewer than 2 regions')
		super().__init__(name, *self.regions, orientation=orientation)
		self.sampler = sampler

	def sampleGiven(self, value):
		regs = [value[reg] for reg in self.regions]
		# Now that regions have been sampled, attempt intersection again in the hopes
		# there is a specialized sampler to handle it (unless we already have one)
		if not self.sampler:
			failed = False
			intersection = regs[0]
			for region in regs[1:]:
				intersection = intersection.intersect(region)
				if isinstance(intersection, IntersectionRegion):
					failed = True
					break
			if not failed:
				intersection.orientation = value[self.orientation]
				return intersection
		return IntersectionRegion(*regs, orientation=value[self.orientation],
		                          sampler=self.sampler, name=self.name)

	def evaluateInner(self, context):
		regs = (valueInContext(reg, context) for reg in self.regions)
		orientation = valueInContext(self.orientation, context)
		return IntersectionRegion(*regs, orientation=orientation, sampler=self.sampler,
		                          name=self.name)

	def containsPoint(self, point):
		return all(region.containsPoint(point) for region in self.regions)

	def uniformPointInner(self):
		sampler = self.sampler
		if not sampler:
			sampler = self.genericSampler
		return self.orient(sampler(self))

	@staticmethod
	def genericSampler(intersection):
		regs = intersection.regions
		point = regs[0].uniformPointInner()
		for region in regs[1:]:
			if not region.containsPoint(point):
				raise RejectionException(
				    f'sampling intersection of Regions {regs[0]} and {region}')
		return point

	def __repr__(self):
		return f'IntersectionRegion({self.regions!r})'

class DifferenceRegion(Region):
	def __init__(self, regionA, regionB, sampler=None, name=None):
		self.regionA, self.regionB = regionA, regionB
		super().__init__(name, regionA, regionB, orientation=regionA.orientation)
		self.sampler = sampler

	def sampleGiven(self, value):
		regionA, regionB = value[self.regionA], value[self.regionB]
		# Now that regions have been sampled, attempt difference again in the hopes
		# there is a specialized sampler to handle it (unless we already have one)
		if not self.sampler:
			diff = regionA.difference(regionB)
			if not isinstance(diff, DifferenceRegion):
				diff.orientation = value[self.orientation]
				return diff
		return DifferenceRegion(regionA, regionB, orientation=value[self.orientation],
		                        sampler=self.sampler, name=self.name)

	def evaluateInner(self, context):
		regionA = valueInContext(self.regionA, context)
		regionB = valueInContext(self.regionB, context)
		orientation = valueInContext(self.orientation, context)
		return DifferenceRegion(regionA, regionB, orientation=orientation,
		                        sampler=self.sampler, name=self.name)

	def containsPoint(self, point):
		return self.regionA.containsPoint(point) and not self.regionB.containsPoint(point)

	def uniformPointInner(self):
		sampler = self.sampler
		if not sampler:
			sampler = self.genericSampler
		return self.orient(sampler(self))

	@staticmethod
	def genericSampler(difference):
		regionA, regionB = difference.regionA, difference.regionB
		point = regionA.uniformPointInner()
		if regionB.containsPoint(point):
			raise RejectionException(
			    f'sampling difference of Regions {regionA} and {regionB}')
		return point

	def __repr__(self):
		return f'DifferenceRegion({self.regionA!r}, {self.regionB!r})'
