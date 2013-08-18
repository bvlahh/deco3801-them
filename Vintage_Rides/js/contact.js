// function used to unsure that the rental start/end & date/time are set by the user

		function ValidateForm() {
			var fname=document.getElementById("fname").value;
			var lname=document.getElementById("lname").value;
			var email=document.getElementById("email").value;
			var phone=document.getElementById("phone").value;	
			
					if (fname==null || fname=="")
						{document.getElementById("fname").style.borderColor="red";	//used to show the user that 'this' field is missing data
						return false;
						}
																		
					if (lname==null || lname=="")
						{document.getElementById("fname").style.border="none";	//removes the red border in the previous field as that is no longer an error 
						document.getElementById("lname").style.borderColor="red";
						return false;
						}
								
					if (email==null || email=="")
						{document.getElementById("lname").style.border="none";
						document.getElementById("email").style.borderColor="red";
						return false;
						}
					
					if (phone==null || phone=="")
						{document.getElementById("email").style.border="none";
						document.getElementById("phone").style.borderColor="red";
						return false;
						}
					
					else
						{document.getElementById("phone").style.border="none";
						document.getElementById("success").style.display="inline"; // notifies user that their information has been sent 
						  };
			};
