// var currentTab = 0; // Current tab is set to be the first tab (0)
// showTab(currentTab); // Display the current tab

// function showTab(n) {
//   // This function will display the specified tab of the form...
//   var x = document.getElementsByClassName("tab");
//   x[n].style.display = "block";
//   //... and fix the Previous/Next buttons:
//   if (n == 0) {
//     document.getElementById("prevBtn").style.display = "none";
//   } else {
//     document.getElementById("prevBtn").style.display = "inline";
//   }
//   if (n == (x.length - 1)) {
//     document.getElementById("nextBtn1").innerHTML = "Submit";
//   } else {
//     document.getElementById("nextBtn1").innerHTML = "הבא";
//   }
//   //... and run a function that will display the correct step indicator:
//   fixStepIndicator(n)
// }

// function nextPrev(n) {
//   // This function will figure out which tab to display
//   var x = document.getElementsByClassName("tab");
//   // Exit the function if any field in the current tab is invalid:
//   // if (n == 1 && !validateForm()) return false;
//   // Hide the current tab:
//   x[currentTab].style.display = "none";
//   // Increase or decrease the current tab by 1:
//   currentTab = currentTab + n;
//   // if you have reached the end of the form...
//   if (currentTab >= x.length) {
//     // ... the form gets submitted:
//     // document.getElementById("contactForm").submit();
//     document.getElementById("nextBtn1").type = "submit";
//     alert( document.getElementById("nextBtn1").type)
//     return false;
//   }
//   // Otherwise, display the correct tab:
//   showTab(currentTab);
// }

// function validateForm() {
// //   // This function deals with validation of the form fields
// //   var x, y, i, valid = true;
// //   x = document.getElementsByClassName("tab");
// //   y = x[currentTab].getElementsByTagName("input");
// //   // A loop that checks every input field in the current tab:
// //   for (i = 0; i < y.length; i++) {
// //     // If a field is empty...
// //     if (y[i].value == "") {
// //       // add an "invalid" class to the field:
// //       y[i].className += " invalid";
// //       // and set the current valid status to false
// //       valid = false;
// //     }
// //   }
//   // If the valid status is true, mark the step as finished and valid:
  
//   document.getElementsByClassName("step")[currentTab].className += " finish";

//   return 1 // return the valid status
// }

// function fixStepIndicator(n) {
//   // This function removes the "active" class of all steps...
//   var i, x = document.getElementsByClassName("step");
//   for (i = 0; i < x.length; i++) {
//     x[i].className = x[i].className.replace(" active", "");
//   }
//   //... and adds the "active" class on the current step:
//   x[n].className += " active";
// }


$(document).ready(function () {
  var counter = 2;

  $("#addrow").on("click", function () {
    var newRow = $("<tr>");
    var cols = "";
    if (counter < 15) {
      cols += '<td><input type="text" class="form-control" name="level_name' + counter + '"/></td>';
      cols += '<td><input type="date" class="form-control" name="level_start' + counter + '"/></td>';
      cols += '<td><input type="date" class="form-control" name="level_end' + counter + '"/></td>';
      cols += '<td><input type="text" class="form-control" name="level_descrip' + counter + '"/></td>';
      cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="מחק"></td>';
      newRow.append(cols);
      $("table.order-list").append(newRow);
      counter++;
    }
    if(counter == 15){
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