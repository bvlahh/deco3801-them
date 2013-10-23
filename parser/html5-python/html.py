#coding=utf-8
import html5lib
from html5lib import treewalkers
from html5lib import treebuilders


error = """
<!DOCTYPE html>
<html><head><title>My First Evaluated Webpage</table></head>
<body><h2>I bet I can sneak in a lower header... or maybe not!</h2><h1>Look at the majesty of my multiple heading ones!!</h1><h1>Wait that's a bad thing</h1><frame>I can use frames, right?</frame><p>Dang, what about leaving a tag open, with a image <img src=""> and no alt text!</body></html>
"""

bigdoc = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    
    <head>
        
        <script type="text/Javascript" src="js/cars.js"></script>
        <script type="text/Javascript" src="js/jquery-1.7.2.min.js"></script>
        <script src="js/lightbox.js"></script>
        <link href="css/lightbox.css" rel="stylesheet" />
        <link rel="stylesheet" href="css/cars.css" type="text/css">
        <link rel="stylesheet" type="text/css" href="css/navigation.css">
        <link rel="stylesheet" type="text/css" href="css/style.css">
        <title>Vintage Rides</title>
        
    </head>
    
    <body>

        <div id="header">
            <div id="titleBar">
            <div id="logoContainer">
            <div id="logo">Vintage Rides</div>
        </div>
        <div id="menuContainer">
        <div id="menu">
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="specialOffers.html">Special Offers</a></li> 
                <li><a href="cars.html">Cars</a></li> 
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>  
            </ul>
        </div>  
        </div>
        </div>
        
        
        <div class="wrapper">
            <br><br><div id="car_nav">
                <ul class="car_nav">
                    <li id="cat_all" class="car_nav" onclick="hideShow('ALL')">ALL</li>
                    <li id="cat_twenties" class="car_nav" onclick="hideShow('twenties')">20s</li>
                    <li id="cat_thirties" class="car_nav" onclick="hideShow('thirties')">30s</li>
                    <li id="cat_fourties" class="car_nav" onclick="hideShow('fourties')">40s</li>
                    <li id="cat_fifties" class="car_nav" onclick="hideShow('fifties')">50s</li>
                    <li id="cat_sixties" class="car_nav" onclick="hideShow('sixties')">60s</li>
                    <li id="cat_seventies" class="car_nav" onclick="hideShow('seventies')">70s</li>
                </ul>
            </div>
            
        
            
            <div id ="twenties">
                <h3>20's Cars</h3>
                
                <div class="carContainer">
                <a href="img/20s/1922 Buick 645 Touring.JPG" rel="lightbox" title="1922 Buick 645 Touring">
                        <img src="img/20s/1922 Buick 645 Touring.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1922 Buick 645 Touring</h4>
                        <p>The Series 23 Buick's rode on a 118-inch wheelbase and were 
                        powered by a four-cylinder engine. They came in a wide variety of 
                        bodystyles including roadster, touring sedan, sedan, and touring. 
                        The Touring bodystyle was the most popular with 45,227 examples 
                        produced. </p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$90.95</h5></div>
                         <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        
                        <a href="img/20s/1929 Cadillac 341B Dual Cowl Phaeton.JPG" rel="lightbox" title="1929 Cadillac 341B Dual Cowl Phaeton">
                        <img src="img/20s/1929 Cadillac 341B Dual Cowl Phaeton.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1929 Cadillac 341B Dual Cowl Phaeton</h4>
                        <p>This was the first Cadillac to feature a Synchromesh transmission 
                        that eliminated the practice of 'double-clutching' while shifting gears. 
                        Other first-time features included security-plate safety glass used 
                        in all windows and the windshield, and electric windshield wipers.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$120.75</h5></div>
                         <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
        </div>
            
            <div id = "thirties">
                <h3>30's Cars</h3>
                <br><div class="carContainer">
                    
                
                        
                        <a href="img/30s/1937 Bugatti.jpg" rel="lightbox" title="1937 Bugatti">
                        <img src="img/30s/1937 Bugatti.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1937 Bugatti Stelvio </h4>
                        <p>Designed by Bugatti, Stelvio bodies were constructed by several 
                        contracted coachbuilders. This example, a 1937 Stelvio offered by 
                        RM Auctions at its Scottsdale sale in 2008, was built by Gangloff.
                         Built for the entire run of Type 57s--from 1934 until the cease of 
                         production in September 1939.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$200.95</h5></div>
                         <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">                  
                        <a href="img/30s/1935 Auburn Speedster.jpg" rel="lightbox" title="1935 Auburn Speedster">
                        <img src="img/30s/1935 Auburn Speedster.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1935 Auburn Speedster</h4>
                        <p>The supercharged Auburn Speedster was introduced in 1935 and 
                        this example was #9 in production. The Speedster was an effort by 
                        designer Gordon Buehrig and engineer August Duesenberg to save 
                        the struggling car company. Alas it turned out to be Auburn's 
                        final glory.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$135.00</h5></div>
                         <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        
                        <a href="img/30s/1931 Buick Series 80.JPG" rel="lightbox" title="1931 Buick Series 80">
                        <img src="img/30s/1931 Buick Series 80.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1931 Buick Series 80</h4>
                        <p>The car is powered by a 344.8 cubic-inch inline eight-cylinder 
                        engine capable of producing just over 100 horsepower. There is a 
                        three-speed synchromesh sliding manual gearbox and four-wheel 
                        mechanical brakes. The car is from the private collection of 
                        Marvin Tamaroff and has been treated to a restoration of the 
                        highest standards.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$110.75</h5></div>
                         <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
            </div>
            
            <div id = "fourties">
                <h3>40's Cars</h3>
                <br><div class="carContainer">
                        <a href="img/40s/1941 Cadillac Convertible.JPG" rel="lightbox" title="1941 Cadillac Convertible">
                        <img src="img/40s/1941 Cadillac Convertible.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1941 Cadillac Convertible</h4>
                        <p>1941 produced another record sales year for Cadillac; sales 
                        topped 66,000, exceeding any previous year by 20,000 units and 
                        trailing rival Packard by only 7,000 cars. However, of that record 
                        number, only 400 were model 62290, the convertible sedan. 
                        This is the last year that General Motors produced a convertible 
                        sedan in any of its model lines</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$120.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/40s/1940 Chrysler Saratoga.JPG" rel="lightbox" title="1940 Chrysler Saratoga">
                        <img src="img/40s/1940 Chrysler Saratoga.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1940 Chrysler Saratoga</h4>
                        <p>The Saratoga nameplate first appeared in 1939 and was applied 
                        to Chrysler's most expensive full-size eight-cylinder models, 
                        above that of the Imperial and the New Yorker. 
                        It was available as a four-door sedan and the Hayes-bodied club coupe.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$120.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/40s/1946 Buick Sedanet 3131.JPG" rel="lightbox" title="1946 Buick Sedanet">
                        <img src="img/40s/1946 Buick Sedanet 3131.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1946 Buick Sedanet</h4>
                        <p>The Roadmaster was an automobile built by the Buick division of 
                        General Motors. Roadmasters produced between 1936 and 1958 were 
                        built on Buick's longest non-limousine wheelbase and shared their 
                        basic structure with entry-level Cadillac and, after 1940, 
                        seniorOldsmobiles</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$120.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
            </div>
            
            <div id = "fifties">
                <h3>50's Cars</h3>
                <br><div class="carContainer">
                        <a href="img/50s/Jaguar XK140.JPG" rel="lightbox" title="Jaguar XK140">
                        <img src="img/50s/Jaguar XK140.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>Jaguar XK140</h4>
                        <p>The XK140 was introduced in late 1954 and sold as a 1955 model. 
                        Exterior changes that distinguished it from the XK120 included more 
                        substantial front and rear bumpers with overriders, and flashing 
                        turn signals (operated by a switch on the dash) above the front 
                        bumper. </p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$180.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/50s/Dodge wagon 1956.jpg" rel="lightbox" title="Dodge Wagon 1956.jpg">
                        <img src="img/50s/Dodge wagon 1956.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1956 Dodge Wagon</h4>
                        <p>One of the most powerful cars in its price range, the Dodge 
                        Coronet for 1954 could be equipped wîth a 150-horsepower, 
                        241-cubic inch Red Ram Hemi V-8 that was introduced the previous year. 
                        The potent engine enabled Dodge to win acclaim during 1954 by 
                        steering numerous AAA Stock Car speed records.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$130.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/50s/1950 DeSoto.JPG" rel="lightbox" title="1950 DeSoto">
                        <img src="img/50s/1950 DeSoto.JPG" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1950 DeSoto</h4>
                        <p>Although Chrysler built seven experimental Town and Country 
                        hardtops for 1946, mass-produced pillarless Mopars didn't begin 
                        until the 1950 model year. DeSoto's version was the 1950 DeSoto 
                        Custom Sportsman, upholstered to convertible standards and built 
                        with all the integrity that distinguished Chrysler products of this period</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$98.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
            </div>
            
            <div id = "sixties">
                <h3>60's Cars</h3>
                <br><div class="carContainer">
                        <a href="img/60s/1964 Ford Tunderbird.jpg" rel="lightbox" title="1964 Ford Tunderbird">
                        <img src="img/60s/1964 Ford Tunderbird.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1964 Ford Thunderbird</h4>
                        <p>Yet another restyled body kicked off the Thunderbird's fourth 
                        three-year run in 1964. Beauty beneath the skin included the same 
                        unitized structure introduced in 1958 and a 300-horsepower 390 V-8 
                        backed by a Cruise-O-Matic automatic transmission. Power steering 
                        and brakes also were standard, as they had been in 1963</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$175.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/60s/Chevrilet Corvair.jpg" rel="lightbox" title="Chevrilet Corvair">
                        <img src="img/60s/Chevrilet Corvair.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>Chevrilet Corvair</h4>
                        <p>As an economy compact, Chevrolet's rear-engine Corvair was too 
                        radical to sell well against Ford's conservatively designed Falcon. 
                        A lithe and lovely car with an air-cooled, flat-six in the back, 
                        a la the VW Beetle - was a handful</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$110.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/60s/1966 Ford Mustang.jpg" rel="lightbox" title="1966 Ford Mustang">
                        <img src="img/60s/1966 Ford Mustang.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>1966 Ford Mustang</h4>
                        <p>There's no doubt that 1966 is one of the most popular 
                        Ford Mustang model years in the history of the car. In fact, 
                        March 1966 marked the creation of the millionth Mustang.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$120.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
            </div>
            
            <div id = "seventies">
                <h3>70's Cars</h3>
                <br><div class="carContainer">
                        <a href="img/70s/ford capri mk1.jpg" rel="lightbox" title="Ford Capri MK1.jpg">
                        <img src="img/70s/ford capri mk1.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>Ford Capri MK1</h4>
                        <p>Front wheel drive, independent suspension (McPherson type at the front), 
                        front disc brakes. The Fiat 127 has all the characteristics for great success. 
                        70 HP ready to take on the Italian roads.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$90.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/70s/FIAT 127.jpg" rel="lightbox" title="FIAT 127">
                        <img src="img/70s/FIAT 127.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>FIAT 127</h4>
                        <p>Front wheel drive, independent suspension (McPherson type at the front), 
                        front disc brakes. The Fiat 127 has all the characteristics for great success. 
                        70 HP ready to take on the Italian roads.</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$70.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
                
                <br><div class="carContainer">
                        <a href="img/70s/Classic Triumph 2000TC.jpg" rel="lightbox" title="Classic Triumph 2000TC">
                        <img src="img/70s/Classic Triumph 2000TC.jpg" height="150" width="200" class="carImage"></a>
                    <div class="carInfo">
                        <h4>Classic Triumph 2000TC</h4>
                        <p>The Triumph 2000 is a mid-sized, rear wheel drive automobile 
                        which was produced in Coventry by the Triumph Motor Companybetween 
                        1963 and 1977. Larger-engined models, known as the Triumph 2.5 PI 
                        and Triumph 2500 were also produced</p>
                    </div>
                    <div class="carPrice">
                        <p>From <br><br><br><br>per day</p><div class="price"><h5>$80.95</h5></div>
                        <button class="bookNow" onclick="alert('OK')">Book Now</button>
                    </div>
                </div>
            </div>
        </div>
        </div>
        </body>
        
            
</html>
"""

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

files = ""
filename = ""

blah = """<html><head><title>ye</title></head><body><frame></frame></body></html>"""

table = """
<html><head></head><body>
<table border="1">
<tr>
<td>row 1, cell 1</td>
<td>row 1, cell 2</td>
</tr>
<tr>
<td>row 2, cell 1</td>
<td>row 2, cell 2</td>
</tr>
</table>
<footer></footer></body></html>
"""
fragment = bigdoc.decode("utf-8")

minidom_document = parser.parse(fragment, files=files, filename=filename)
# <html><html><body><body></body></body></html></html>
# <html><html><head><head></head></head></html></html>
# <html><html><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><html></html><body></html></html>
#<html><html><head><html></html></head></html></html>
#<html><html><head><html></html></head><footer></footer></html></html>
#<html></head><head><body></head><body></body></html>

# Causes a number of undefined errors.
#<html><*body></body /></body></html>

def parseAgain():
    minidom_document = parser.parse(fragment, files=files, filename=filename)


walker = treewalkers.getTreeWalker("etree")
stream = walker(minidom_document)

print '---------------------'

#print fragment

print '---------------------'

for error in parser.errors:
	print error

print '---------------------'

print parser.parseErrors()

print '---------------------'

#for item in stream:
	#print item
