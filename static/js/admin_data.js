var speed = 10;

/* Call this function with a string containing the ID name to
 * the element containing the number you want to do a count animation on.*/
function incEltNbr(id) {
  elt = document.getElementById(id);
  endNbr = Number(document.getElementById(id).innerHTML);
  incNbrRec(0, endNbr, elt);
}

/*A recursive function to increase the number.*/
function incNbrRec(i, endNbr, elt) {
  if (i <= endNbr) {
    elt.innerHTML = i;
    setTimeout(function() {//Delay a bit before calling the function again.
      incNbrRec(i + 1, endNbr, elt);
    }, speed);
  }
}



incEltNbr("nbr1"); /*Call this funtion with the ID-name for that element to increase the number within*/
incEltNbr("nbr2");
incEltNbr("nbr3");
incEltNbr("nbr4");
incEltNbr("nbr5");
incEltNbr("nbr6");
incEltNbr("nbr7");
incEltNbr("nbr8");
incEltNbr("nbr9");

