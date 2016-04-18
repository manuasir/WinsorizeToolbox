import arcpy
import scipy.stats


class Toolbox(object):
    def __init__(self):
        self.label = "myToolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Winsorize]


class Winsorize(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Winsorize"
        self.description = ""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        entrada = arcpy.Parameter(
            displayName="Entrada",
            name="entrada",
            datatype="Feature Layer",
            parameterType="Required",
            direction="Input")

        # Sinuosity Field parameter
        winsorize_field = arcpy.Parameter(
            displayName="Winsorize Field",
            name="winsorize_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")

        # winsorize_field.value = "winsorize"
        # winsorize_field.columns = [['Field', 'Fields'], ['Long', 'Ranks']]

        # # Derived Output Features parameter
        # out_features = arcpy.Parameter(
        #     displayName="Salida",
        #     name="salida",
        #     datatype="Field",
        #     parameterType="Derived",
        #     direction="Output")
        percentil = arcpy.Parameter(
            displayName="Percentil",
            name="percentil",
            datatype="Long",
            parameterType="Required",
            direction="Input")
        # winsorize_field.parameterDependencies = [winsorize_field.name]
        winsorize_field.parameterDependencies = [entrada.name]
        # arcpy.AddField_management(entrada, "nuevoCampo", "LONG", 9, "", "", "refcode", "NULLABLE", "REQUIRED")
        parameters = [entrada,winsorize_field,percentil]

        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True


    def updateParameters(self, parameters):

        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        tabla = parameters[0].valueAsText
        campo = parameters[1].valueAsText
        percentil_entero = parameters[2].valueAsText

        percentil = float(percentil_entero)/100
        mylist = [(0.0)]
        i=0
        index=0
        rows = arcpy.SearchCursor(tabla)

        row = rows.next()
        while row:
            mylist.insert(index,row.getValue(campo))
            index=index+1
            row = rows.next()
        resultado = scipy.stats.mstats.winsorize(mylist, limits=percentil)
        fieldList = arcpy.ListFields(tabla)
        fieldName = [f.name for f in fieldList]

        field = "Winsor"
        if field in fieldName:
            arcpy.AddError("NO VA.".format(input))
            raise arcpy.ExecuteError
        else:
            arcpy.AddField_management(tabla, field, "TEXT")

            cursor = arcpy.UpdateCursor(tabla)
            row = cursor.next()
            while row:
                # field2 will be equal to field1 multiplied by 3.0
                row.setValue(field, resultado[i])
                cursor.updateRow(row)
                row = cursor.next()
                i=i+1
        del row
        del rows

        # mylist = [(0.0)]

        # index=0
        # row = rows.next()
        # while row:
        #       # print row.size
        # #     #value_table.addRow(row)
        #     mylist.insert(index,row)
        #     index=index+1
        #     row = rows.next()
        # print len(mylist)
        return
