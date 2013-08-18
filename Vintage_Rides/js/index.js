//function to allow user to set their rental start&end date.  

$(function datepicker() {
    $( "#sdate,#edate" ).datepicker({ minDate: 0, dateFormat: 'dd/mm/yy'});
	});

//function to allow user to specify at what time they'll need the car and for how many hours (so price can be calculated) 

$(function timepicker() {
	$("#SetTime1,#SetTime2").timepicker({ 'minTime': '8:00am', 'maxTime': '5:00pm', });
	});
		

// function used to unsure that the rental start/end & date/time are set by the user

		function ValidateForm() {
			var startDate=document.getElementById("sdate").value;
			var endDate=document.getElementById("edate").value;
			var stime=document.getElementById("SetTime1").value;
			var etime=document.getElementById("SetTime2").value;	
			
					if (startDate==null || startDate=="")
						{document.getElementById("sdate").style.borderColor="red";	//used to show the user that 'this' field is missing data
						return false;
						}
																		
					if (endDate==null || endDate=="")
						{document.getElementById("sdate").style.border="none";	//removes the red border in the previous field as that is no longer an error 
						document.getElementById("edate").style.borderColor="red";
						return false;
						}
								
					if (stime==null || stime=="")
						{document.getElementById("edate").style.border="none";
						document.getElementById("SetTime1").style.borderColor="red";
						return false;
						}
					
					if (etime==null || etime=="")
						{document.getElementById("SetTime1").style.border="none";
						document.getElementById("SetTime2").style.borderColor="red";
						return false;
						}
					
					else
						{document.getElementById("SetTime2").style.border="none";
						document.getElementById("success").style.display="inline"; // notifies user that their information has been sent 
						  };
			};

// function used for featured cars
		
		var slideShowSpeed = 3000;
		var crossFadeDuration = 3;
		var Pic = new Array();

		Pic[0] = 'images/featured/1.png'
		Pic[1] = 'images/featured/2.png'
		Pic[2] = 'images/featured/3.png'
		
		
		var t;
		var j = 0;
		var p = Pic.length;
		var preLoad = new Array();
		for (i = 0; i < p; i++) {
		preLoad[i] = new Image();
		preLoad[i].src = Pic[i];
		}
		
		function javaSlideShow() {
		if (document.all) {
		document.images.SlideShow.style.filter="blendTrans(duration=2)";
		document.images.SlideShow.style.filter="blendTrans(duration=crossFadeDuration)";
		document.images.SlideShow.filters.blendTrans.Apply();
		}
		document.images.SlideShow.src = preLoad[j].src;
		if (document.all) {
		document.images.SlideShow.filters.blendTrans.Play();
		}
		j = j + 1;
		if (j > (p - 1)) j = 0;
		t = setTimeout('javaSlideShow()', slideShowSpeed);
		}



//function used to make a 'slideshow' out of the divs found in the parent div (#testimonial) 

$(function testimonial(){
    $ds = $('#testimonial div');
    $ds.hide().eq(0).show();	//only shows the 1st div and hides the rest
    setInterval(function(){
        $ds.filter(':visible').fadeOut(function(){
            var $div = $(this).next('div');
            if ( $div.length == 0 ) {
                $ds.eq(0).fadeIn();
            } else {
                $div.fadeIn();
            }
        });
    }, 5000);	//3seconds; duration of each slide  
});