var isAfterStartDate = function(startDateStr, endDateStr) {
    var inDate = new Date(startDateStr),
        eDate = new Date(endDateStr);

    if(inDate < eDate) {
        return true;
    }

};

var isSameName = function(newProjectName) {
    var allNames = document.getElementsByName("names");
    for(var i = 0; i < allNames.length; i++){
        if(allNames[i].value == newProjectName) {
            return false;
        }
    
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

    jQuery.validator.addMethod("isSameName", function(value, element) {

        return isSameName($('#name').val(), value);
    }, "קיים פרוייקט בשם זה, נא לבחור שם אחר.");



    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2,
                    isSameName: true,
                },
                subject: {
                    required: true,
                   
                },
                start_date: {
                    required: true,
                },
                end_date: {
                    required: true,
                    isAfterStartDate: true
                },
                message: {
                    required: true,
                    minlength: 20
                },
            },
            messages: {
                name: {
                    required: "נא לבחור שם לפרוייקט.",
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
                    required: "בחרו תאריך התחלה",
                    
                },

                end_date: {
                    required: "בחרו תאריך הגשה",
                }
            },
            submitHandler: function(form) {
                // $("#nextBtn1").click(function () {
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $(form).serialize(),
                    url: "/new_project/"+ document.getElementsByName("user_ajax")[0].value,
                    success: function() {
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');
                            alert("הפרוייקט נוסף למערכת. ניתן לצפות בו במסך הפרוייקטים.");
                            window.location.href = "/projects/" + document.getElementsByName("user_ajax")[0].value;
                        })
                    },
                    error: function() {

                        $('#contactForm').fadeTo( "slow", 1, function() {
                            // $('#error').fadeIn()
                            // $('.modal').modal('hide');
		                	// $('#error').modal('show');
                        })
                    }
                })
            } 
            
        })
    })
        
 })(jQuery)
})