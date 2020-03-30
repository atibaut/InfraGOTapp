'''
InfraGOTApp: module for database management (PostgreSQL)
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 
@version 1.0
'''

# ## LIBRARIES in use
from __future__ import absolute_import, print_function

from datetime import datetime

from pony import options
from pony.orm import *

# library for PostgreSQL
# library for Pony ORM 
options.CUT_TRACEBACK = False
# ##

# create database object
db = Database()
# output all SQL queries to stdout (console), False = don't output to stdout
sql_debug(True)

# connection parameters for the PostegreSQL database (use yours parameters!)
params = dict(
    postgres=dict(provider='postgres', user='andrejt', password='jidaki42.', host='localhost', database='InfraGOTdb'),
)

# connect to the PostgreSQL database
db.bind(**params['postgres'])

# CLASSES for database tables 


class IfcActor(db.Entity):
    """According to the 
https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifckernel/lexical/ifcactor.htm
Organization(s) contracted to fulfill the order, typically a single contractor, subcontractor, or supplier."""
    id = PrimaryKey(int)
    theActor = Required('IfcPersonAndOrganization')


class IfcActorRole(db.Entity):
    id = PrimaryKey(int, auto=True)
    role = Required('IfcRoleEnum')
    userDefinedRole = Optional(str, nullable=True)  # if none of the RoleEnum applies
    description = Optional(str, nullable=True)
    personAndOrganization = Set('IfcPersonAndOrganization')


class IfcRoleEnum(db.Entity):
    """https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifcactorresource/lexical/ifcroleenum.htm"""
    id = PrimaryKey(int)
    constant = Required(str)
    description = Optional(str, nullable=True)
    actorRole = Set(IfcActorRole)


class IfcPersonAndOrganization(db.Entity):
    id = PrimaryKey(int, auto=True)
    theperson = Required('IfcPerson')
    theorganization = Required('IfcOrganization')
    roles = Required(IfcActorRole)
    ifcactor = Optional(IfcActor)
    relOwnerHistory = Optional('IfcOwnerHistory')


class IfcPerson(db.Entity):
    identification = PrimaryKey(str, auto=True)
    familyName = Required(str)
    givenName = Required(str)
    middleNames = Optional(str, nullable=True)
    prefixTitles = Optional(str)
    suffixTitles = Optional(str)
    roles = Optional(str)
    adresses = Optional(str)
    personAndOrganization = Set(IfcPersonAndOrganization)


class IfcOrganization(db.Entity):
    identification = PrimaryKey(str, auto=True)
    name = Required(str)
    description = Optional(str, nullable=True)
    roles = Optional(str)
    addresses = Optional(str, nullable=True)
    personAndOrganization = Set(IfcPersonAndOrganization)
    relApplication = Required('IfcApplication')


class IfcReferent(db.Entity):
    """An object that Identifies physical location (linear placement) for single measurement"""
    id = PrimaryKey(int, auto=True)
    ownerHistory = Optional(str)
    name = Optional(str)
    description = Optional(str)
    objectType = Optional(str)
    objectPlacement = Required('IfcLinearPlacement')
    representation = Optional(str)
    predefinedType = Required('IfcReferentTypeEnum')
    restartDistance = Optional(float)
    relPerformanceHistory = Set('IfcRelAssignsToPerformanceHistory')


class IfcPavement(db.Entity):
    id = PrimaryKey(int, auto=True)
    relRoad = Set('IfcRelAggregatesToRoad')
    relCourse = Set('IfcRelAggregatesCourseToPavement')


class IfcCourse(db.Entity):
    id = PrimaryKey(int, auto=True)
    ownerHistory = Optional(str)
    name = Optional(str)
    description = Optional(str)
    objectType = Optional(str)
    objectPlacement = Optional(str)
    representation = Required('IfcProductDefinitionShape')
    tag = Optional(str)
    pavement = Set('IfcRelAggregatesCourseToPavement')


class IfcProject(db.Entity):
    id = PrimaryKey(int, auto=True)
    globalId = Required(str)
    ownerHistory = Optional('IfcOwnerHistory')
    name = Optional(str, nullable=True)
    description = Optional(str, nullable=True)
    objectType = Optional(str, nullable=True)
    longName = Optional(str, nullable=True)
    phase = Optional(str, nullable=True)
    representationContexts = Optional('IfcGeometricRepresentationContext')
    unitsInContext = Optional(str, nullable=True)
    relDocument = Set('IfcRelAggregatessDocumentToProject')
    relSite = Set('IfcRelAggregatessToProject')


class IfcSite(db.Entity):
    id = PrimaryKey(int, auto=True)
    ownerHistory = Optional(str)
    name = Optional(str)
    description = Optional(str)
    objectType = Optional(str)
    objectPlacement = Optional(str)
    representation = Optional(str)
    longName = Optional(str)
    compositionType = Optional(str)
    refLatitude = Optional(str)
    refLongitude = Optional(str)
    refElevation = Optional(str)
    landTitleNumber = Optional(str)
    siteAddress = Optional(str)
    relProject = Set('IfcRelAggregatessToProject')
    relFacility = Set('IfcRelAggregatesToSite')


class IfcRoad(db.Entity):
    id = PrimaryKey(int, auto=True)
    relFacility = Set('IfcRelAggregatesToFacility')
    relAlignment = Set('IfcRelContainedInSpatialStructure')
    relatedPavement = Set('IfcRelAggregatesToRoad')


class IfcBridge(db.Entity):
    id = PrimaryKey(int, auto=True)
    ownerHistory = Optional(str)
    name = Optional(str)
    description = Optional(str)
    objectType = Optional(str)
    objectPlacement = Optional(str)
    representation = Optional(str)
    longName = Optional(str)
    compositionType = Optional(str)
    predefinedType = Optional(str)


class IfcRail(db.Entity):
    id = PrimaryKey(int, auto=True)


class IfcTunnel(db.Entity):
    id = PrimaryKey(int, auto=True)


class IfcRelAggregatesToSite(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatingSite = Required(IfcSite)
    relatedFacility = Required('IfcFacility')


class IfcFacility(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(str)
    relSite = Set(IfcRelAggregatesToSite)  # https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifcproductextension/lexical/ifcfacility.htm
    relRoad = Set('IfcRelAggregatesToFacility')
    compositionType = Optional(str)


class IfcRelContainedInSpatialStructure(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatingRoad = Required(IfcRoad)
    relatedAlignment = Required('IfcAlignment')


class IfcAlignment(db.Entity):
    id = PrimaryKey(int, auto=True)
    ownerHistory = Optional(str)
    name = Optional(str)
    description = Optional(str)  # Alignment
    objectType = Optional(str)
    objectPlacement = Optional('IfcLocalPlacement')
    representation = Optional(str)
    axis = Required('IfcAlignmentCurve')
    predefinedType = Optional(str)
    relRoad = Set(IfcRelContainedInSpatialStructure)


class IfcReferentTypeEnum(db.Entity):
    """https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/schema/ifcproductextension/lexical/ifcreferenttypeenum.htm"""
    id = PrimaryKey(int, auto=True)
    constant = Required(str)
    description = Optional(str)
    ifcReferent = Optional(IfcReferent)


class IfcRelAggregatesToFacility(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatingFacility = Required(IfcFacility)
    relatedRoad = Required(IfcRoad)


class IfcRelAggregatessToProject(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatingProject = Required(IfcProject)
    relatedSite = Required(IfcSite)


class IfcOwnerHistory(db.Entity):
    id = PrimaryKey(int, auto=True)
    owningUser = Required(IfcPersonAndOrganization)
    owningApplication = Required('IfcApplication')
    state = Optional(str)
    changeAction = Optional(str)
    lastModifiedDate = Optional(str)
    lastModifyingUser = Optional(str)
    lastModifyingApplication = Optional(str)
    creationDate = Optional(datetime)
    relIfcProject = Optional(IfcProject)


class IfcApplication(db.Entity):
    id = PrimaryKey(int, auto=True)
    applicationDeveloper = Set(IfcOrganization)
    version = Optional(str)
    applicationFullName = Optional(str)
    applicationIdentifier = Optional(str)
    relOwnerHistory = Optional(IfcOwnerHistory)


class IfcAlignmentCurve(db.Entity):
    id = PrimaryKey(int, auto=True)
    horizontal = Required('IfcAlignment2DHorizontal')
    vertical = Required('IfcAlignment2DVertical')
    tag = Optional(str)
    alignment = Optional(IfcAlignment)
    relIfcOffsetCurveByDistancess = Set('IfcOffsetCurveByDistances')
    relIfcSectionedSolidHorizontal = Optional('IfcSectionedSolidHorizontal')
    relIfcLinearPlacement = Optional('IfcLinearPlacement')


class IfcRelAggregatesToRoad(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatingRoad = Required(IfcRoad)
    relatedPavement = Required(IfcPavement)


class IfcRelAggregatesCourseToPavement(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatedCourse = Required(IfcCourse)
    relatingPavement = Required(IfcPavement)


class IfcDistanceExpressionCBD(db.Entity):
    id = PrimaryKey(int, auto=True)
    distanceAlong = Required(float)
    offsetLateral = Optional(float)
    offsetVertical = Optional(float)
    offsetLongitudinal = Optional(float)
    alongHorizontal = Optional(bool)
    relIfcfOffsetCurveByDistance = Required('IfcOffsetCurveByDistances')


class IfcOffsetCurveByDistances(db.Entity):
    id = PrimaryKey(int, auto=True)
    offsetValues = Set(IfcDistanceExpressionCBD)
    tag = Optional(str)
    relIfcAlignmentCurve = Required(IfcAlignmentCurve)
    relIfcGeometricCurveSet = Required('IfcGeometricCurveSet')


class IfcProductDefinitionShape(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(str)
    representations = Set('IfcShapeRepresentation')
    relCourse = Optional(IfcCourse)


class IfcShapeRepresentation(db.Entity):
    id = PrimaryKey(int, auto=True)
    contextOfItems = Required('IfcGeometricRepresentationContext')
    representationIdentifier = Optional(str)
    representationType = Optional(str)
    itemsSectionedSolid = Set('IfcSectionedSolidHorizontal')
    itemsGeometricCurveSet = Set('IfcGeometricCurveSet')
    relProductDefinitionShape = Required(IfcProductDefinitionShape)


class IfcSectionedSolidHorizontal(db.Entity):
    id = PrimaryKey(int, auto=True)
    directrix = Required(IfcAlignmentCurve)
    crossSections = Set('IfcArbitraryClosedProfileDef')
    crossSectionPositions = Set('IfcDistanceExpressionSSH')
    fixedAxisVertical = Required(bool, default=True)
    relShapeRepresentation = Required(IfcShapeRepresentation)


class IfcArbitraryClosedProfileDef(db.Entity):
    id = PrimaryKey(int, auto=True)
    profileType = Required(str, default='AREA')  # file:///Users/andrejt/GoogleDrive.AT/PhD_GO_Sara/IFC/IFC_schema/IFC4x3_FilesBSMART_082019/Material%20For%20Review/IR-ROAD-WP3_IFC-SchemaExtension_draft/ifc4x3-ifc-road-first-draft/html/schema/ifcprofileresource/lexical/ifcprofiletypeenum.htm / in our case AREA
    profileName = Optional(str)
    outerCurve = Required('IfcIndexedPolyCurve')
    relSectionedSolidHorizontal = Required(IfcSectionedSolidHorizontal)


class IfcIndexedPolyCurve(db.Entity):
    id = PrimaryKey(int, auto=True)
    points = Set('IfcCartesianPointList2D')
    segments = Set('IfcSegmentIndexSelect')
    selfIntersect = Optional(bool)  # file:///Users/andrejt/GoogleDrive.AT/PhD_GO_Sara/IFC/IFC_schema/IFC4x3_FilesBSMART_082019/Material%20For%20Review/IR-ROAD-WP3_IFC-SchemaExtension_draft/ifc4x3-ifc-road-first-draft/html/index.htm / iin our case False
    relArbitraryClosedProfileDef = Optional(IfcArbitraryClosedProfileDef)


class IfcCartesianPointList2D(db.Entity):
    id = PrimaryKey(int, auto=True)
    coordList = Set('CoordinatesList2D')
    tagList = Set('TagList')
    relIndexedPolyCurve = Required(IfcIndexedPolyCurve)


class IfcGeometricRepresentationContext(db.Entity):
    id = PrimaryKey(int, auto=True)
    contextIdentifier = Optional(str)
    contextType = Optional(str)
    coordinateSpaceDimension = Required(int)
    precision = Optional(float)
    worldCoordinateSystem = Required('IfcAxis2Placement3D')
    trueNorth = Optional(str)
    relIfcShapeRepresentation = Optional(IfcShapeRepresentation)
    relIfcProject = Required(IfcProject)


class IfcCartesianPointCS2D(db.Entity):
    id = PrimaryKey(int, auto=True)
    x = Required(float)
    y = Required(float)
    z = Required(float)
    relCurveSegment2D = Optional('IfcCurveSegment2D')


class IfcSegmentIndexSelect(db.Entity):
    """see this for more explanation and example: https://github.com/opensourceBIM/BIMserver/issues/902"""
    id = PrimaryKey(int, auto=True)
    order = Optional(str)
    relIndexedPolyCurve = Required(IfcIndexedPolyCurve)
    relLineIndexs = Set('IfcLineIndex')


class IfcLineIndex(db.Entity):
    id = PrimaryKey(int, auto=True)
    firstIndex = Optional(int)
    lastIndex = Optional(int)
    relIfcSegmentIndexSelect = Required(IfcSegmentIndexSelect)


class CoordinatesList2D(db.Entity):
    id = PrimaryKey(int, auto=True)
    x = Required(float)
    y = Required(float)
    relCartesianPointList2D = Required(IfcCartesianPointList2D)


class TagList(db.Entity):
    id = PrimaryKey(int, auto=True)
    tag = Required(str)
    relCartesianPointList2D = Required(IfcCartesianPointList2D)


class IfcAlignment2DHorizontal(db.Entity):
    id = PrimaryKey(int, auto=True)
    startDistAlong = Optional(str)
    segments = Set('IfcAlignment2DHorizontalSegment')
    relIfcAlignmentCurve = Optional(IfcAlignmentCurve)


class IfcCurveSegment2D(db.Entity):
    id = PrimaryKey(int, auto=True)
    startPoint = Required(IfcCartesianPointCS2D)
    startDirection = Required(float)
    segmentLength = Required(float)
    relIfcAlignment2DHorizontalSegment = Optional('IfcAlignment2DHorizontalSegment')


class IfcTransitionCurveType(db.Entity):
    id = PrimaryKey(int, auto=True)
    constant = Optional(str)
    description = Optional(str)
    relIfcITtransitionCurveSegments2D = Set('IfcTransitionCurveSegment2D')


class IfcLocalPlacement(db.Entity):
    id = PrimaryKey(int, auto=True)
    placementRelTo = Optional(str)
    relativePlacement = Required('IfcAxis2Placement3D')
    relIfcAlignment = Optional(IfcAlignment)


class IfcAxis2Placement3D(db.Entity):
    id = PrimaryKey(int, auto=True)
    location = Required('IfcCartesianPoint')
    axis = Optional('IfcDirectionAxis', reverse='relIfcAxis2Placement3D1')
    refDirection = Optional('IfcDirectionAxis', reverse='relIfcAxis2Placement3D2')
    relIfcGeometricRepresentationContext = Optional(IfcGeometricRepresentationContext)
    relIfcLocalPlacement = Optional(IfcLocalPlacement)


class IfcDirectionAxis(db.Entity):
    id = PrimaryKey(int, auto=True)
    x = Required(float)
    y = Required(float)
    z = Required(float)
    relIfcAxis2Placement3D1 = Optional(IfcAxis2Placement3D, reverse='axis')
    relIfcAxis2Placement3D2 = Optional(IfcAxis2Placement3D, reverse='refDirection')


class IfcCircularArcSegment2D(IfcCurveSegment2D):
    radius = Required(float)
    isCCW = Required(bool)


class IfcLineSegment2D(IfcCurveSegment2D):
    pass


class IfcTransitionCurveSegment2D(IfcCurveSegment2D):
    startRadius = Optional(str)
    endRadius = Optional(str)
    isStartRadiusCCW = Required(bool)
    isEndRadiusCCW = Required(bool)
    transitionCurveType = Required(IfcTransitionCurveType)


class IfcGeometricCurveSet(db.Entity):
    id = PrimaryKey(int, auto=True)
    relShapeRepresentation = Required(IfcShapeRepresentation)
    elements = Set(IfcOffsetCurveByDistances)


class IfcLinearPlacement(db.Entity):
    id = PrimaryKey(int, auto=True)
    PlacementRelTo = Optional(str)
    placementMeasuredAlong = Required(IfcAlignmentCurve)
    distance = Required('IfcDistanceExpressionLinearPlacement')
    orientation = Required('IfcOrientationExpression')
    cartesianPosition = Optional(str)
    relIfcReferent = Optional(IfcReferent)


class IfcOrientationExpression(db.Entity):
    id = PrimaryKey(int, auto=True)
    lateralAxisDirection = Required(float)
    verticalAxisDirection = Required(float)
    reiifcLinearPlacement = Optional(IfcLinearPlacement)


class IfcPerformanceHistory(db.Entity):
    """IfcControl"""
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(str)
    identification = Optional(str)
    lifeCyclePhase = Required(str)
    predefinedType = Required('IfcPerformanceHistoryTypeEnum')
    controls = Set('IfcRelAssignsToPerformanceHistory')
    isDefinedBy = Set('IfcRelDefinesByProperties')  # IsDefinedBy


class IfcRelAssignsToPerformanceHistory(db.Entity):
    """IfcRelAssignsToControl"""
    id = PrimaryKey(int, auto=True)
    relReferent = Required(IfcReferent)  # relatedObjects
    relPerformanceHistory = Required(IfcPerformanceHistory)  # relatingControl


class IfcPerformanceHistoryTypeEnum(db.Entity):
    id = PrimaryKey(int, auto=True)
    constant = Optional(str)
    description = Optional(str)
    relPerformanceHistory = Set(IfcPerformanceHistory)


class IfcRelDefinesByProperties(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(str)
    relatedObjectPerformanceHistory = Required(IfcPerformanceHistory)
    relatingPropertyDefinition = Required('IfcPropertySet')


class IfcPropertySet(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(str)
    definesOccurrence = Set(IfcRelDefinesByProperties)
    hasProperties = Set('IfcPropertyReferenceValue')


class IfcPropertyReferenceValue(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    partOfPset = Required(IfcPropertySet)
    usageName = Optional(str)
    propertyReference = Optional('IfcIrregularTimeSeries')


class IfcIrregularTimeSeries(db.Entity):
    id = PrimaryKey(int, auto=True)
    relPropertyReferenceValue = Required(IfcPropertyReferenceValue)
    name = Required(str)
    description = Optional(str)
    startTime = Required(datetime)
    endTime = Required(datetime)
    timeSeriesDataType = Required('IfcTimeSeriesDataTypeEnum')
    dataOrigin = Required('IfcDataOriginEnum')
    userDefinedDataOrigin = Optional(str)
    unit = Optional(str)
    values = Set('IfcIrregularTimeSeriesValue')


class IfcDistanceExpressionLinearPlacement(db.Entity):
    id = PrimaryKey(int, auto=True)
    distanceAlong = Required(float)
    offsetLateral = Optional(float)
    offsetVertical = Optional(float)
    offsetLongitudinal = Optional(float)
    alongHorizontal = Optional(bool)
    relLinearPlacement = Optional(IfcLinearPlacement)


class IfcDistanceExpressionSSH(db.Entity):
    id = PrimaryKey(int, auto=True)
    distanceAlong = Required(float)
    offsetLateral = Optional(float)
    offsetVertical = Optional(float)
    offsetLongitudinal = Optional(float)
    alongHorizontal = Optional(float)
    relSectionedSolidHorizontal = Required(IfcSectionedSolidHorizontal)


class IfcCartesianPoint(db.Entity):
    id = PrimaryKey(int, auto=True)
    x = Required(float)
    y = Required(float)
    z = Required(float)
    relIfcAxis2Placement3D = Optional(IfcAxis2Placement3D)


class IfcTimeSeriesDataTypeEnum(db.Entity):
    id = PrimaryKey(int, auto=True)
    constant = Required(str)
    description = Required(str)
    relIfcIrregularTimeSeries = Set(IfcIrregularTimeSeries)


class IfcDataOriginEnum(db.Entity):
    id = PrimaryKey(int, auto=True)
    constant = Required(str)
    description = Required(str)
    relIfcIrregularTimeSeries = Set(IfcIrregularTimeSeries)


class IfcIrregularTimeSeriesValue(db.Entity):
    id = PrimaryKey(int, auto=True)
    timeStamp = Required(str)
    listValues = Set('MeasureValue')
    relIfcIrregularTimeSeries = Required(IfcIrregularTimeSeries)


class MeasureValue(db.Entity):
    id = PrimaryKey(int, auto=True)
    measureValue = Required(float)
    relMeasureValue = Required(IfcIrregularTimeSeriesValue)


class Document(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    type = Optional(str)
    version = Optional(str)
    timeStamp = Optional(datetime)
    content = Optional(LongStr)
    relIfcProject = Set('IfcRelAggregatessDocumentToProject')


class IfcRelAggregatessDocumentToProject(db.Entity):
    id = PrimaryKey(int, auto=True)
    relatedDocument = Required(Document)
    relatingProject = Required(IfcProject)


class IfcAlignment2DVertical(db.Entity):
    id = PrimaryKey(int, auto=True)
    segments = Set('IfcAlignment2DVerticalSegment')
    relIfcAlignmentCurve = Optional(IfcAlignmentCurve)


class IfcAlignment2DSegment(db.Entity):
    id = PrimaryKey(int, auto=True)
    tangentialContinuity = Optional(bool)
    startTag = Optional(str)
    endTag = Optional(str)


class IfcAlignment2DHorizontalSegment(IfcAlignment2DSegment):
    curveGeometry = Required(IfcCurveSegment2D)
    relIfcAlignment2DHorizontal = Required(IfcAlignment2DHorizontal)


class IfcAlignment2DVerticalSegment(IfcAlignment2DSegment):
    startDistAlong = Optional(float)
    horizontalLength = Optional(float)
    startHeight = Optional(float)
    startGradient = Optional(float)
    relIfcAlignment2DVertical = Required(IfcAlignment2DVertical)


class IfcAlignment2DVerSegParabolicArc(IfcAlignment2DVerticalSegment):
    parabolaConstant = Required(float)
    isConvexPa = Required(bool)


class IfcAlignment2DVerSegLine(IfcAlignment2DVerticalSegment):
    pass


class IfcAlignment2DVerSegCircularArc(IfcAlignment2DVerticalSegment):
    radius = Required(float)
    isConvexCa = Required(bool)
####

#### METHODS


# creates tables in the database
def create_tables():
    db.generate_mapping(create_tables=True)

# method that inputs/creates new data objects in the database  
# @db_session
# def populate_database():
#     if Person.select().first():
#         return  # already populated

#     p = Person(name='Person1', ssn='SSN1')
#     g = Group(number=123)
#     prof1 = Professor(name='Professor1', salary=1000, position='position1', ssn='SSN5')
#     prof2 = Professor(name='Andrej Tibaut', salary=3000, position='Assoc. Prof.', ssn='SSN42')
#     a1 = Assistant(name='Assistant1', group=g, salary=100, ssn='SSN4', mentor=prof1)
#     a2 = Assistant(name='Assistant2', group=g, salary=200, ssn='SSN6', mentor=prof2)
#     s1 = Student(name='Student1', group=g, ssn='SSN2', mentor=prof2)
#     s2 = Student(name='Student2', group=g, ssn='SSN3')
#     commit()  # add data to the database


@db_session
def storeDocument(docName, docType, docContent, docVersion, timeStamp):
    d = Document(name=docName, type=docType, content=docContent, version=docVersion, timeStamp=timeStamp)
#     g = Group(number=123)
#     prof1 = Professor(name='Professor1', salary=1000, position='position1', ssn='SSN5')
#     prof2 = Professor(name='Andrej Tibaut', salary=3000, position='Assoc. Prof.', ssn='SSN42')
#     a1 = Assistant(name='Assistant1', group=g, salary=100, ssn='SSN4', mentor=prof1)
#     a2 = Assistant(name='Assistant2', group=g, salary=200, ssn='SSN6', mentor=prof2)
#     s1 = Student(name='Student1', group=g, ssn='SSN2', mentor=prof2)
#     s2 = Student(name='Student2', group=g, ssn='SSN3')
#     commit()  # add data to the database
    return d




@db_session
def storeIfcProject(project, docid):
    if project is None:
        return None
    doc = Document.get(id=docid)
    p = IfcProject(globalId=project.GlobalId, name=project.Name, description=project.Description, phase="maintenance", longName=project.LongName)
    rel = IfcRelAggregatessDocumentToProject(relatedDocument=doc, relatingProject=p)
               

def show_all_measured_values():
    print();
    for obj in MeasureValue.select():
        print('measured value', obj)
        for attr in obj._attrs_:
            print(attr.name, "=", attr.__get__(obj))
        print()
        
        
# program flow
# if __name__ == '__main__':
#create_tables()
#     populate_database()
    
#     with db_session:
# #        show_all_persons()
#         s1 = Student.get(name='Student1')
#         if s1 is None:
#             print('Student1 not found')
#         else:
#             mentor = s1.mentor
#             print(mentor.name, 'is mentor of Student1')
#             print('Is he assistant?', isinstance(mentor, Assistant))
#         print()
#  
#         for s in Student.select(lambda s: s.mentor.salary == 1000):
#             print(s.name)

