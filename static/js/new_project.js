$(document).ready(function () {
  var counter = 2;

  function minDateOfStart() {
    var lastEndDate = document.getElementsByName("level_end" + (counter - 1))[0].value;
    return lastEndDate
  }


  function getMax() {
    var projectEnd = document.getElementsByName("end_date")[0].value;
    return projectEnd;
  }

  function checkDates(){
    var start =  document.getElementsByName("level_start" + (counter - 1))[0].value;
    var end =  document.getElementsByName("level_end" + (counter - 1))[0].value;
    startD = new Date(start);
    endD = new Date(end);
    if (startD > endD){
      alert("תאריך ההתחלה של השלב חייב להיות מוקדם מתאריך הסיום.")
      return false;
    }
    return true;
  }

  function disableLast() {
    var levelStart = document.getElementsByName("level_start" + (counter - 1))[0];
    var levelEnd = document.getElementsByName("level_end" + (counter - 1))[0];
    levelStart.disabled = true;
    levelEnd.disabled = true;
  }


  $("#addrow").on("click", function () {
    var newRow = $("<tr>");
    var cols = "";
    var dateInput1 = document.getElementsByName("level_start" + (counter - 1))[0].value;
    var dateInput2 = document.getElementsByName("level_end" + (counter - 1))[0].value;
 
    if (counter < 15 && dateInput1.length != 0 && dateInput2 != 0 && checkDates()) {
      disableLast();
      cols += '<td><input required type="text" class="form-control" name="level_name' + counter + '"/></td>';
      cols += '<td><input type="date"' + 'min ="' + minDateOfStart() + '"max ="' + getMax() +
       '" required class="form-control" name="level_start' + counter + '"/></td>';
      cols += '<td><input type="date"' + 'min ="' + minDateOfStart() + '"max ="' + getMax() +
      '"required class="form-control" name="level_end' + counter + '"/></td>';
      cols += '<td><input required type="text" class="form-control" name="level_descrip' + counter + '"/></td>';
      cols += '<td><input required type="button" class="ibtnDel btn btn-md btn-danger "  value="מחק"></td>';

      newRow.append(cols);
      $("table.order-list").append(newRow);
      counter++;
    }
    if (counter == 15) {
      document.getElementById("addrow").value = "לא ניתן להוסיף עוד שלבים.";
    }

  });



  $("table.order-list").on("click", ".ibtnDel", function (event) {
    $(this).closest("tr").remove();
    counter -= 1
  });


});



function calculateRow(row) {
  var price = +row.find('input[name^="price"]').val();

}

function calculateGrandTotal() {
  var grandTotal = 0;
  $("table.order-list").find('input[name^="price"]').each(function () {
    grandTotal += +$(this).val();
  });
  $("#grandtotal").text(grandTotal.toFixed(2));
}

