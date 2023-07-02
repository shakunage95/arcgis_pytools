from imp import reload
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import arcpy

arcpy.env.workspace="E:\\文档\\ArcGIS\\temp\\"

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [MulticalGeodesicArea,AreaAdjustment]


class MulticalGeodesicArea(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "计算图斑地类面积"
        self.description = "用于计算图斑地类面积"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 =  arcpy.Parameter(
        displayName="面要素图层",
        name="source_layer",
        datatype=["GPLayer","GPPolygon"],
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="扣除系数字段",
        name="deduction_factor",
        datatype="Field",
        parameterType="Required",
        direction="Input")
        param1.parameterDependencies = [param0.name]

        param2 = arcpy.Parameter(
        displayName="图斑面积字段",
        name="gross_area",
        datatype="Field",
        parameterType="Optional",
        direction="Input")
        param2.parameterDependencies = [param0.name]

        param3 = arcpy.Parameter(
        displayName="扣除面积字段",
        name="deduction_area",
        datatype="Field",
        parameterType="Optional",
        direction="Input")
        param3.parameterDependencies = [param0.name]

        param4 = arcpy.Parameter(
        displayName="图斑地类面积字段",
        name="net_area",
        datatype="Field",
        parameterType="Optional",
        direction="Input")
        param4.parameterDependencies = [param0.name]

        params=[param0,param1,param2,param3,param4]
        self.params=params
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        if not arcpy.Describe(parameters[0]).shapeType == "Polygon":
            arcpy.AddError("source_layer must be polygon")
            raise arcpy.ExecuteError("source_layer must be polygon")
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        p0=parameters[0].value		# source_layer
        p1=parameters[1].valueAsText	# DeductionFactor
        p2=parameters[2].valueAsText	# GrossArea
        p3=parameters[3].valueAsText	# DeductionArea
        p4=parameters[4].valueAsText	# NetArea

        fields=arcpy.ListFields(p0)
        if not p2:
            p2="GrossArea"
            if not p2 in [f.name for f in fields]:
                arcpy.AddField_management(p0, p2, "DOUBLE","","","")

        express='round(!shape.geodesicArea!,2)'
        arcpy.CalculateField_management(p0, p2, 
                               express , "PYTHON_9.3")

        if not p3:
            p3="DeductionArea"
            if not p3 in [f.name for f in fields]:
                arcpy.AddField_management(p0, p3, "DOUBLE","","","")

        express1='round(!'+p1+'!*!'+p2+'!,2)'
        arcpy.CalculateField_management(p0, p3, 
                              express1 , "PYTHON_9.3")

        if not p4:
            p4="NetArea"
            if not p4 in [f.name for f in fields]:
                arcpy.AddField_management(p0, p4, "DOUBLE","","","")

        express2='round(!'+p2+'!-!'+p3+'!,2)'
        arcpy.CalculateField_management(p0, p4, 
                              express2 , "PYTHON_9.3")

        arcpy.AddField_management(p0, "TMP", "DOUBLE","","","")
        arcpy.DeleteField_management(p0, "TMP")

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()

        return



class AreaAdjustment(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "图斑面积平差"
        self.description = "图斑面积平差"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 =  arcpy.Parameter(
        displayName="面要素图层",
        name="source_layer",
        datatype=["GPLayer","GPPolygon"],
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="图斑面积字段",
        name="area",
        datatype="Field",
        parameterType="Required",
        direction="Input")
        param1.parameterDependencies = [param0.name]

        param2 = arcpy.Parameter(
        displayName="下发指标面积",
        name="issue_area",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input")

        params=[param0,param1,param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if not arcpy.Describe(parameters[0]).shapeType == "Polygon":
            arcpy.AddError("source_layer must be polygon")
            raise arcpy.ExecuteError("source_layer must be polygon")

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # 创建临时mdb存储汇总数据
        #arcpy.CreateTable_management()

        # 汇总统计数据
        #arcpy.Statistics_analysis(intable, outtable, stats)


        # 删除临时mdb
        #arcpy.Delete_management(out.mdb)

        return
