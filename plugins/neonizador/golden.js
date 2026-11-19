// Huellas de referencia: node golden.js <raiz_repo> [k1,k2] > huellas.json
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const ROOT=path.resolve(process.argv[2]||"."), KS=(process.argv[3]||"0.5").split(",").map(Number);
const {GROUPS,render}=require(ROOT+"/src/engine/effects.js"), TEX=require(ROOT+"/src/engine/textures_node.js")(ROOT+"/plugin/tex");
const W=1200,H=852,raw=fs.readFileSync(ROOT+"/tools/dev/mask1200.raw"),M=new Float32Array(W*H); for(let i=0;i<M.length;i++)M[i]=raw[i]/255;
const out={mascara:"tools/dev/mask1200.raw (1200x852)",semilla:3,opciones:"fondo y ambiente activados, color original",huellas:{}};
for(const g of GROUPS)for(const fx of g.variants)for(const k of KS){const t0=Date.now();const r=render(fx.id,M,W,H,{intensity:k,seed:3,tex:TEX});out.huellas[fx.id+"@"+k]=crypto.createHash("md5").update(Buffer.from(r.rgba.buffer||r.rgba)).digest("hex");process.stderr.write(fx.id+" "+k+" "+(Date.now()-t0)+"ms\n");}
console.log(JSON.stringify(out,null,1));
