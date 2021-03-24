var isAfterStartDate = function (startDateStr, endDateStr) {
    var inDate = new Date(startDateStr),
        eDate = new Date(endDateStr);

    if (inDate < eDate) {
        return true;
    }

};

var isValidEditStart = function (pStart) {
    levels = document.getElementsByName("level");
    for (var i = 0; i < levels.length; i++) {
        var strLevel = levels[i].value;
        var data = strLevel.split(",");
        sDate = new Date(data[0]);
        pStart = new Date(pStart);
        isDone = data[1];
        if (sDate < pStart && isDone == "False") {
            return false;
        }

    }
    return true;
};

var isValidEditEnd = function (pEnd) {
    levels = document.getElementsByName("level");
    for (var i = 0; i < levels.length; i++) {
        var strLevel = levels[i].value;
        var data = strLevel.split(",");
        eDate = new Date(data[2]);
        pEnd = new Date(pEnd);
        isDone = data[1];
        alert(eDate);
        alert(pEnd);
        alert(eDate > pEnd && isDone == "False");
        if (eDate > pEnd && isDone == "False") {
            return false;
        }

    }
    return true;
};

var isSameName = function (newProjectName) {
    var allNames = document.getElementsByName("names");
    for (var i = 0; i < allNames.length; i++) {
        alert(allNames[i].value);
        alert(allNames[i].value == newProjectName);
        if (allNames[i].value == newProjectName) {
            return false;
        }

    }
    return true;

};

$(document).ready(function () {

    (function ($) {
        "use strict";


        jQuery.validator.addMethod('answercheck', function (value, element) {
            return this.optional(element) || /^\bcat\b$/.test(value)
        }, "type the correct answer -_-");

        jQuery.validator.addMethod("isAfterStartDate", function (value, element) {

            return isAfterStartDate($('#start_date').val(), value);
        }, "תאריך הסיום צריך להיות לאחר תאריך ההתחלה.");

        jQuery.validator.addMethod("isValidEditStart", function (value, element) {

            return isValidEditStart($('#start_date').val(), value);
        }, "לא ניתן להחיל את השינוי כיוון שתאריך ההתחלה החדש מבטל שלבים בפרויקט. יש לשנות את השלבים או למחוק אותם.");

        jQuery.validator.addMethod("isValidEditEnd", function (value, element) {

            return isValidEditEnd($('#end_date').val(), value);
        }, "לא ניתן להחיל את השינוי כיוון שתאריך הסיום החדש מבטל שלבים בפרויקט. יש לשנות את השלבים או למחוק אותם.");

        jQuery.validator.addMethod("isSameName", function(value, element) {

            return isSameName($('#name').val(), value);
        }, "קיים פרוייקט בשם זה, נא לבחור שם אחר.");
    
        // validate contactForm form
        $(function () {
            $('#projectEdit').validate({
                rules: {
                    name: {
                        required: false,
                        minlength: 2,
                        isSameName: true,
                    },
                    subject: {
                        required: false,

                    },
                    start_date: {
                        required: false,
                        isValidEditStart: true,


                    },
                    end_date: {
                        required: false,
                        isAfterStartDate: true,
                        isValidEditEnd: true,

                    },
                    message: {
                        required: false,
                        minlength: 10
                    }
                },
                messages: {
                    name: {

                        minlength: "שם הפרוייקט חייב להיות לפחות 2 תווים"
                    },
                    subject: {
                        required: "נא לבחור מקצוע"

                    },

                    message: {
                        required: "נא לכתוב תיאור לפרוייקט",
                        minlength: "זה הכל?"

                    },

                    start_date: {
                        required: "בחרו תאריך התחלה"
                    },

                    end_date: {
                        required: "בחרו תאריך הגשה"
                    }
                },
                submitHandler: function (form) {

                    $(form).ajaxSubmit({
                        type: "POST",
                        data: $(form).serialize(),
                        url: "/project_edit",
                        success: function () {

                            $('.alert').alert()
                            $('#projectEdit :input').attr('disabled', 'disabled');

                            $('#projectEdit').fadeTo("slow", 1, function () {
                                $(this).find(':input').attr('disabled', 'disabled');
                                $(this).find('label').css('cursor', 'default');
                                $('#success').fadeIn()
                                $('.modal').modal('hide');
                                $('#success').modal('show');
                                alert("העדכון הושלם.")
                                // window.location.href ='/project_edit';
                            })
                        },
                        error: function () {
                            $('#projectEdit').fadeTo("slow", 1, function () {
                                $('#error').fadeIn()
                                $('.modal').modal('hide');
                                $('#error').modal('show');
                            })
                        }
                    })
                } //********************* */

            })
        })

    })(jQuery)
})
