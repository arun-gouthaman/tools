//UI Creation
function UI(){
    win = new Window('dialog', 'save .png .tga');
    win.txtPnl = win.add('panel', undefined, 'Enter Layer Set names');
    win.txtPnl.msgEdt = win.txtPnl.add('edittext', [0,0,300,40], readtxtFile()[0], {multiline:true});
    win.txtPnl.saveMessageSt = win.txtPnl.add('statictext', [0,75,300,90], 'Save Path' );
    win.txtPnl.pathEdt = win.txtPnl.add('edittext', [0,0,300,20], readtxtFile()[1], {multiline:false});
    win.txtPnl.versionMessageSt = win.txtPnl.add('statictext', undefined, 'Maya Version' );
    win.txtPnl.versionMessageSt.alignment = 'left'
    win.txtPnl.versionEdt = win.txtPnl.add('edittext', [0,0,50,18], readtxtFile()[2], {multiline:false});
    win.txtPnl.versionEdt.alignment = 'left'
    win.txtPnl.chk1 = win.txtPnl.add('checkbox', undefined, 'Update textures in Maya');
    win.txtPnl.saveBtn = win.txtPnl.add('button', undefined, 'Save',{name:'save'});
    win.txtPnl.saveBtn.onClick = run;
    win.show()
    }


function finalAlert(){
    alert('ENTER THE RIGHT DATA HUMAN');
    tryVal = 0;
    }


function readUsrData(){
    tryVal = 0
    usrName = Folder('~').fsName.match(/[^\\]+$/);
    docPath = "C:\\Users\\"+usrName+"\\Documents";
    docPath = docPath + "\\PhotoshopTemp"
    outputFolder = new Folder(docPath);
    pathFile = new File(docPath+"\\pathFile.txt");
    }


function readtxtFile(){
    var fileTxt = ""
    if(!outputFolder.exists || !pathFile.exists){
        return(['Enter LayerSet Names', 'Enter Path','2014'])
        }

    pathFile.open('r');

    while(!pathFile.eof)

    fileTxt += pathFile.readln();
    
    pathFile.close();
    
    var PathLayer = fileTxt.split(';');
    return PathLayer
    }


function writePathFile(usrPth, usrLayer, mayaVer){
    if(!outputFolder.exists){
        outputFolder.create()
        }
    
    pathFile.open('w');

    pathFile.writeln(usrLayer +';'+ usrPth +';'+mayaVer);

    pathFile.close();
    
    
    
    }



function run(){
    
    
    //Get User input LayerSet names
    var getText = win.txtPnl.msgEdt.text 
    
    
    
    
    //if no text entered display alert message and terminate execution
    if (getText.length == 0){
        alert('Please Enter LayerSet Names ' + usrName);
        return;
        }
    
       
    var getSavePath = win.txtPnl.pathEdt.text
    if (getSavePath.length == 0){
        alert('Please enter Valid Path ' + usrName);
        return;
        }
    
    var mayaVersion = win.txtPnl.versionEdt.text
    if(mayaVersion.length == 0){
        alert('Please Enter maya version ' + usrName)
        return
        }
    
    mayaVerChk = new Folder("\\C\\Program Files\\Autodesk\\Maya"+mayaVersion)
    if(!mayaVerChk.exists){
        alert('Maya'+mayaVersion+'does not exist ' + usrName);
        return;
        }
    
    
    destFldr = new Folder(getSavePath)
    if(!destFldr.exists){
        alert('Path does not exist ' + usrName);
        return;
        }
    
    
    writePathFile(getSavePath, getText, mayaVersion)
    
    //get rid of spaces between names
    getText = getText.split(' ').join('');
    
    
    

    
    //Split user input for layer names
    var names = getText.split(',')
    
    var docRef = app.activeDocument;
    
    //obtain filename and file path to save files
    var fileNm = docRef.name;
    fileNm = fileNm.replace(".psd", "");
    
 
    //Call function to hide all existing layers
    hideLayers(docRef);
    
    //targa and png options 
    pngSaveOptions = new PNGSaveOptions();
    pngSaveOptions.compression = 9;
    targaSaveOptions = new TargaSaveOptions();
    targaSaveOptions.alphaChannels = true;
    targaSaveOptions.rleCompression = true;
    
    //loop through number of LayerSet and call outPut function to save the file
    for (var i=0 ; i<names.length ; i++){
        outPut(docRef,names[i], pngSaveOptions, targaSaveOptions, getSavePath, fileNm)
        }
    
    //close UI after saving
    closeWindow()
    
    
    //Call function to create batch file
    checked = win.txtPnl.chk1.value
    if (checked){
        var fileNameParam = getText
        CreateFile(fileNameParam, getSavePath, mayaVersion)
        }

    }

//Hide All Layers except background layer
function hideLayers(docRef){
    var numberOfLayers = docRef.layers.length;
    for(var i=0 ; i<numberOfLayers; i++){
        var layerName = String(docRef.layers[i]);
        if (layerName.indexOf("Background") == -1 ){
            docRef.layers[i].visible = 0;
        }
    }
    }


//Save Layers to output folder
function outPut(docRef, lyrSets, pngSaveOptions, targaSaveOptions, savePath, fileNm){
    try{
        //if the LayerSet to be saved is invisible, change it's visibility
        if (docRef.layerSets[lyrSets].visible == false){
            docRef.layerSets[lyrSets].visible = true
            }
        //Save file to output path
        var saveFile = File(savePath + "/"+fileNm+"_"+lyrSets+".png")
        pngSaveOptions = new PNGSaveOptions();
        docRef.saveAs(saveFile, pngSaveOptions, true, Extension.LOWERCASE);
        var saveFile = File(savePath + "/"+fileNm+"_"+lyrSets+".tga")
        targaSaveOptions = new TargaSaveOptions();
        docRef.saveAs(saveFile, targaSaveOptions, true, Extension.LOWERCASE);
        
        docRef.layerSets[lyrSets].visible = false
        }
    catch(error){
        //Display error message
        //alert(error +'\n"'+lyrSets + '"' + '\n save operation will be skipped for ' + lyrSets);
        alert('Error occured\n Save operation will be skipped for ' + lyrSets);
        }

    }

//function to close UI
function closeWindow(){
    //$.writeln('CLOSING UI')
    win.close()
    }

function CreateFile(fileNameParam, savePath, mayaVer){
    var batFile = new File(savePath+'//run.bat');
	if (parseInt(mayaVer) > 2014)
	{
		cmd = "SET PATH=%PATH%;C:\\Program Files\\Autodesk\\Maya"+mayaVer+"\\bin\ncd C:\\Users\\Arun\\Documents\\maya\\"+mayaVer+"\\scripts\nC:\nmayapy mayaSocket.py "+fileNameParam;
	}
	else
	{
		cmd = "SET PATH=%PATH%;C:\\Program Files\\Autodesk\\Maya"+mayaVer+"\\bin\ncd C:\\Users\\Arun\\Documents\\maya\\"+mayaVer+"-x64\\scripts\nC:\nmayapy mayaSocket.py "+fileNameParam;
	}
	batFile.open('w');
    batFile.writeln(cmd);
    batFile.close();
    batFile.execute()
    //batFile.remove()
    }

readUsrData()
readtxtFile()
//readPathFile()
UI()
