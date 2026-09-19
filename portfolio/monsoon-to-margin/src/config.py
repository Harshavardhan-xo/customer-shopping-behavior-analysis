CITIES={"Chennai":(13.0827,80.2707),"Bengaluru":(12.9716,77.5946),"Hyderabad":(17.385,78.4867),"Mumbai":(19.076,72.8777),"Delhi":(28.6139,77.209),"Pune":(18.5204,73.8567),"Kolkata":(22.5726,88.3639)}
BANDS=[("none",0,2.5),("light",2.5,15),("moderate",15,64.5),("heavy",64.5,115.5),("very_heavy",115.5,float("inf"))]
D={"none":(1,0,0,1),"light":(1.08,2,.01,.97),"moderate":(1.22,6,.035,.90),"heavy":(1.40,14,.08,.75),"very_heavy":(1.55,24,.15,.60)}
BASE_ORDERS=4200; BASE_DELIVERY=13.; BASE_CANCEL=.025; AOV=390.; SURGE=85.; SLA=22.; SEED=42