function setMin() {
    //Sets the min date of the first project level. 
    //disables the start date field.
    //Creates a copy of the start date input value, to send to the server.
    var projectStart = document.getElementsByName("start_date")[0];
    var firstLevelStart = document.getElementsByName("level_start1")[0];
    var firstLevelEnd = document.getElementsByName("level_end1")[0];
    var start_val = document.getElementsByName("start_val")[0];
    firstLevelStart.setAttribute("min", projectStart.value);
    if(projectStart.value != ""){
        start_val.value = projectStart.value;
        projectStart.readOnly = true;
    }
}

function setMax() {
    //Sets the max date of all project levels. 
    //disables the end date field, enables the other date fields in the first level.
    //Creates a copy of the end date input value, to send to the server.
    var projectEnd = document.getElementsByName("end_date")[0];
    var projectStart = document.getElementsByName("start_date")[0];
    var firstLevelStart = document.getElementsByName("level_start1")[0];
    var firstLevelEnd = document.getElementsByName("level_end1")[0];
    var end_val = document.getElementsByName("end_val")[0];
    firstLevelStart.setAttribute("max", projectEnd.value);
    firstLevelEnd.setAttribute("max", projectEnd.value); 
    if(projectEnd.value != "" && projectEnd.value > projectStart.value){  
        end_val.value = projectEnd.value;
        projectEnd.readOnly = true;
        firstLevelStart.readOnly = false;
        firstLevelEnd.readOnly = false;
    }
}

function setMinEnd() {
    //Sets the min value of the end date.
    var levelStart = document.getElementsByName("level_start1")[0];
    var levelEnd = document.getElementsByName("level_end1")[0];
    levelEnd.setAttribute("min", levelStart.value);
    if (levelStart.value != ""){
        levelStart.readOnly= true;
    }
}

function disableEnd(){
    // Disables the level End field.
    var levelEnd = document.getElementsByName("level_end1")[0];
    levelEnd.readOnly = true;
}

function clearFields(){
    //Clearing the fields of the first level in the table. 
    var levelStart = document.getElementsByName("level_start1")[0];
    var levelEnd = document.getElementsByName("level_end1")[0];
    var lName = document.getElementsByName("level_name1")[0];
    var lDescrip = document.getElementsByName("level_descrip1")[0];
    lName.value = " ";
    levelStart.value = " ";
    levelEnd.value = " ";
    lDescrip.value = " "; 
    levelStart.readOnly = false;
    levelEnd.readOnly = false;
}


