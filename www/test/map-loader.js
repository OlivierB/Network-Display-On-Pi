// Classe mère 
var classeMere = Class.create({ 
	this.attribut = attribut1; 
	methodeA : function() { 
		// code 
	} 
	methodeB : function() {
	 // code 
	}	 
}); 

var classeFilleExtendsMere = Class.create(classeMere, {
	// Ajout d'une nouvelle méthode 
	methodeC : function() { 
		// code 
	} 
} // Et ça marche ! 

var newObjet = new classeFilleExtendsMere() 

newObjet.methodeA(); 