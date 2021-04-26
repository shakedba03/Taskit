var isAfterStartDate = function(startDateStr, endDateStr) {
    var inDate = new Date(startDateStr),
        eDate = new Date(endDateStr);

    if(inDate <= eDate) {
        return true;
    }

};

var isValidEditStart = function(lStart) {
    var lStart = new Date(lStart);
    var pInfo = document.getElementsByName("project_str")[0].value;
    pInfo = pInfo.split(",");
    var pStart = new Date(pInfo[0]);
    if(pStart > lStart){
        return false;
    }
    return true;

};

var isValidEditEnd = function(lEnd) {
    var lEnd = new Date(lEnd);
    var pInfo = document.getElementsByName("project_str")[0].value;
    pInfo = pInfo.split(",");
    var pEnd = new Date(pInfo[1]);
    if(pEnd < lEnd){
        return false;
    }
    return true;

};

$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    jQuery.validator.addMethod("isAfterStartDate", function(value, element) {

        return isAfterStartDate($('#start_date').val(), value);
    }, "תאריך הסיום צריך להיות לאחר תאריך ההתחלה.");

    jQuery.validator.addMethod("isValidEditStart", function(value, element) {

        return isValidEditStart($('#start_date').val(), value);
    }, "לא ניתן להחיל את השינוי כיוון שתאריך ההתחלה החדש מוקדם מתאריך התחלת הפרויקט.");

    jQuery.validator.addMethod("isValidEditEnd", function(value, element) {

        return isValidEditEnd($('#end_date').val(), value);
    }, "לא ניתן להחיל את השינוי כיוון שתאריך הסיום החדש מאוחר מתאריך סיום הפרויקט.");

    // validate contactForm form
    $(function() {
        $('#levelEdit').validate({
            rules: {
                name: {
                    required: false,
                    minlength: 2
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
            submitHandler: function(form) {
                
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $(form).serialize(),
                    url:"/level_edit",
                    success: function() {
                        
                        $('.alert').alert()
                        $('#levelEdit :input').attr('disabled', 'disabled');
                        
                        $('#levelEdit').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');
                            alert("העדכון הושלם.")
                            window.location.href ='/projects';
                        })
                    },
                    error: function() {
                        $('#levelEdit').fadeTo( "slow", 1, function() {
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
