function hideShow(id){
	
	if(id=="ALL"){
		document.getElementById("twenties").style.display = 'block';
		document.getElementById("thirties").style.display = 'block';
		document.getElementById("fourties").style.display = 'block';
		document.getElementById("fifties").style.display = 'block';
		document.getElementById("sixties").style.display = 'block';
		document.getElementById("seventies").style.display = 'block';
	
	}else if(id == "twenties"){
		document.getElementById("twenties").style.display = 'block';
		document.getElementById("thirties").style.display = 'none';
		document.getElementById("fourties").style.display = 'none';
		document.getElementById("fifties").style.display = 'none';
		document.getElementById("sixties").style.display = 'none';
		document.getElementById("seventies").style.display = 'none';
	
	}else if(id == "thirties"){
		document.getElementById("twenties").style.display = 'none';
		document.getElementById("thirties").style.display = 'block';
		document.getElementById("fourties").style.display = 'none';
		document.getElementById("fifties").style.display = 'none';
		document.getElementById("sixties").style.display = 'none';
		document.getElementById("seventies").style.display = 'none';
		
	}else if(id == "fourties"){
		document.getElementById("twenties").style.display = 'none';
		document.getElementById("thirties").style.display = 'none';
		document.getElementById("fourties").style.display = 'block';
		document.getElementById("fifties").style.display = 'none';
		document.getElementById("sixties").style.display = 'none';
		document.getElementById("seventies").style.display = 'none';
		
	}else if(id== "fifties"){
		document.getElementById("twenties").style.display = 'none';
		document.getElementById("thirties").style.display = 'none';
		document.getElementById("fourties").style.display = 'none';
		document.getElementById("fifties").style.display = 'block';
		document.getElementById("sixties").style.display = 'none';
		document.getElementById("seventies").style.display = 'none';
		
	}else if(id== "sixties"){
		document.getElementById("twenties").style.display = 'none';
		document.getElementById("thirties").style.display = 'none';
		document.getElementById("fourties").style.display = 'none';
		document.getElementById("fifties").style.display = 'none';
		document.getElementById("sixties").style.display = 'block';
		document.getElementById("seventies").style.display = 'none';
		
	}else if(id== "seventies"){
		document.getElementById("twenties").style.display = 'none';
		document.getElementById("thirties").style.display = 'none';
		document.getElementById("fourties").style.display = 'none';
		document.getElementById("fifties").style.display = 'none';
		document.getElementById("sixties").style.display = 'none';
		document.getElementById("seventies").style.display = 'block';
		
	}
	
}

