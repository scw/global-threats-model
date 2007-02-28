Attribute VB_Name = "WriteFilePaths2txt"

'Description:  This code reads all of the datasets in the current ArcMap document
'and writes out the list of datasources to a text file.  The text file is saved with the same
'name (*.txt at the end) and in the same directory as your mxd project.
'This code is an adaptation of VBA code written by Kirk Kuykendall, Kathrin Hutton and Jennifer McCollom, thanks....
'Gerry Gabrisch, www.gabrisch.us



Sub ListSources()

Dim pDocDatasets As IDocumentDatasets
Dim pEnumDS As IEnumDataset
Dim pDS As IDataset
Dim pDLayer As IDataLayer
Dim fs As Object
Dim a As Object
Dim pWdApp As Object
Dim pWdDoc As Object

Set pDocDatasets = ThisDocument
Set pEnumDS = pDocDatasets.Datasets
pEnumDS.Reset


'check to see if the project is saved, exit if not
If GetMXDName = "NotSaved" Then
    MsgBox "This is not a saved project.  Please " & _
    "save the project before running this script.", vbOKOnly, "Error!"
    Exit Sub
End If
   
'creating the object to hold the new text file??  actually not sure.
Set fs = CreateObject("Scripting.FileSystemObject")
'create the text file with the same name as the mxd file
Set a = fs.CreateTextFile(GetMXDName, True)

'loop through the datasets and write the line in the newly created text file
Set pDS = pEnumDS.Next
Do Until pDS Is Nothing

    If TypeOf pDS Is IDataLayer Then
        
        Set pDLayer = pDS    'QI
        If TypeOf pDLayer.DataSourceName Is IDatasetName Then
            a.WriteLine pDS.Name 'new line from 200503
            a.WriteLine pDS.Category 'new line from 200503
            a.WriteLine GetPath(pDLayer.DataSourceName) ' & vbNewLine
	    a.WriteLine pDS.Workspace.PathName
        Else
            a.WriteLine pDS.Name & " is not a datasetname"
        End If
    Else
        a.WriteLine pDS.Name & " is not an IDataLayer"
    End If
    Set pDS = pEnumDS.Next
Loop

'close the text file for editing
a.Close

MsgBox "Sources listed in: " & GetMXDName, vbOKOnly, "Process Completed!"



End Sub

Function GetPath(pDSName As IDatasetName) As String
    GetPath = pDSName.WorkspaceName.PathName
    If TypeOf pDSName Is IFeatureClassName Then
        Dim pFCName As IFeatureClassName
        Set pFCName = pDSName
        If Not pFCName.FeatureDatasetName Is Nothing Then
            GetPath = GetPath & "\" & pFCName.FeatureDatasetName.Name
        End If
    End If
    GetPath = GetPath & "\" & pDSName.Name
End Function

Function GetMXDName() As String
    ' each project in the VBE has a pathname
    Dim pVBProj As VBProject
    Dim FileNTemp() As String
    Dim l As Long, strPath As String
    
    Set pVBProj = ThisDocument.VBProject
    
    ' loop through all the projects
    For l = 1 To pVBProj.VBE.VBProjects.Count ' 1 based
        On Error Resume Next
        strPath = pVBProj.VBE.VBProjects.Item(l).filename
        If Err <> 0 Then
            strPath = ""
            Err.Clear
        End If
        If InStr(1, strPath, ".mxd") > 0 Then
            FileNTemp = Split(strPath, ".mxd")
            GetMXDName = FileNTemp(0) & ".txt"
            Exit Function
        End If
    Next l
    GetMXDName = "NotSaved"
End Function
