"use strict";


// corrijo modulo para que trabaje con negativos
Number.prototype.mod = function(n) {
	return ((this % n) + n) % n;
};

// alfabeto a-z más espacio y coma
const letras = Array.apply(0, Array(26)).map((e, i) =>
	String.fromCharCode("a".charCodeAt(0) + i)
);
letras.push(' ');
letras.push(',');

const letras_r = letras.reduce((acc,e,i) => { acc[e] = i; return(acc); },{});

const enigma = (discos, reflector, texto) => {
	// función de apoyo
	const inverso = disco => {
		const r = Array.apply(0, Array(disco.length));
		disco.map((x, i) => (r[x] = i));
		return r;
	};

	// Ojo, el disco con menor índice es el más a la derecha (el primero que gira), por lo que debo entrar por el más alto
	const discos_r = [...discos].reverse();

	// necesito los discos invertidos para volver del reflector
	const discos_inv = [...discos].map(d => inverso(d));

	// guardo la división de cuando girar, cada disco gira una ve cuando se ha completado la pitatoria de los largos de los discos a su izquierda
	const divs = discos_r.map((d, j) => {
		return discos_r
			.slice(discos_r.length - j)
			.map(sd => {
				return sd.length;
			})
			.reduce((acc, e) => {
				return acc * e;
			}, 1);
	});
	
	// guardo el giro en que van los discos, al principio 0
	const offsets = new Array(discos.length).fill(0);

	const cipher = texto.split("").map((l, i) => {
		//verifico si soporto el caracter 
		if (letras_r[l.toLowerCase()] == undefined) {
			throw new Error("Caracter no soportado: "+l);
		}

		// transformo las letras a números (empezando con a = 0)
		let p = letras_r[l.toLowerCase()];

		// calculo para la letra que voy (i) cuanto debo girar cada disco
		discos_r.map((d, j) => {
			offsets[j] = Math.floor(i / divs[j]);
		});

		// paso de ida por los discos
		discos_r.forEach((d, j) => {
			p = (d[(p + offsets[j]).mod(d.length)] - offsets[j]).mod(d.length);
		});

		// paso por el reflector
		p = reflector[p];

		// paso de vuelta por los discos
		discos_inv.forEach((d, j) => {
			p = (
				d[(p + offsets[discos_inv.length - j - 1]).mod(d.length)] -
				offsets[discos_inv.length - j - 1]
			).mod(d.length);
		});

		return letras[p];
	});

	return cipher.join("");
};

const discos = [
[16,5,23,24,17,14,1,22,21,12,3,6,15,18,4,13,19,25,0,10,27,11,9,20,8,7,2,26],
[17,6,19,11,23,2,21,13,27,9,18,24,0,4,8,26,12,5,14,1,16,7,3,22,15,10,25,20],
[23,22,3,25,16,6,24,4,11,8,20,10,7,26,14,2,15,12,17,21,19,13,0,9,5,18,1,27],
[4,22,26,16,19,0,9,2,14,3,24,13,1,15,18,12,21,17,23,7,11,6,20,27,8,10,5,25],
[18,26,20,14,2,23,16,17,25,3,15,21,1,7,10,19,22,8,5,13,24,11,4,6,9,0,12,27],
[5,21,27,24,17,8,19,3,6,23,2,12,13,14,25,1,0,4,26,7,9,10,22,20,11,18,15,16]
];

const reflector = [1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14,17,16,19,18,21,20,23,22,25,24,27,26]

const plain = "hola ha sido muy grato poder encriptar esta cuestion, aunque no estoy muy seguro que funcione";
console.log("antes de encriptar:", plain);
const cipher = enigma(discos, reflector, plain);
console.log("texto cifrado:", cipher);
const plain2 = enigma(discos, reflector, cipher);
console.log("después de desencriptar:", plain2);
