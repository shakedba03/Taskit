$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2
                },
                subject: {
                    required: true,
                   
                },
                start_date: {
                    required: true,
                    
                },
                end_date: {
                    required: true,
                    
                },
                message: {
                    required: true,
                    minlength: 20
                }
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
                    required: "בחרו תאריך התחלה"
                },

                end_date: {
                    required: "בחרו תאריך הגשה"
                }
            },
            submitHandler: function(form) {
                // $("#nextBtn1").click(function () {
                $(form).ajaxSubmit({
                    type:"POST",
                    data: $(form).serialize(),
                    url:"/new_project",
                    success: function() {
                        
                        $('#contactForm :input').attr('disabled', 'disabled');
                        $('#contactForm').fadeTo( "slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor','default');
                            $('#success').fadeIn()
                            $('.modal').modal('hide');
		                	$('#success').modal('show');
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
            } //********************* */
            
        })
    })
        
 })(jQuery)
})
