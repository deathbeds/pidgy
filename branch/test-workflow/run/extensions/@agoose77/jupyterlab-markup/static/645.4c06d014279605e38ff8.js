"use strict";(self.webpackChunk_agoose77_jupyterlab_markup=self.webpackChunk_agoose77_jupyterlab_markup||[]).push([[645],{645:e=>{e.exports=function(e){var t=e.utils.isSpace;function n(e,t){var n,r,s=e.bMarks[t]+e.tShift[t],i=e.eMarks[t];return s>=i||126!==(r=e.src.charCodeAt(s++))&&58!==r||s===(n=e.skipSpaces(s))||n>=i?-1:s}e.block.ruler.before("paragraph","deflist",(function(e,r,s,i){var a,d,o,p,k,l,u,f,b,h,c,C,_,g,m,I,y,S,v,M;if(i)return!(e.ddIndent<0)&&n(e,r)>=0;if((b=r+1)>=s)return!1;if(e.isEmpty(b)&&++b>=s)return!1;if(e.sCount[b]<e.blkIndent)return!1;if((d=n(e,b))<0)return!1;u=e.tokens.length,v=!0,(M=e.push("dl_open","dl",1)).map=l=[r,0],p=r,o=b;e:for(;;){for(S=!1,(M=e.push("dt_open","dt",1)).map=[p,p],(M=e.push("inline","",0)).map=[p,p],M.content=e.getLines(p,p+1,e.blkIndent,!1).trim(),M.children=[],M=e.push("dt_close","dt",-1);;){for((M=e.push("dd_open","dd",1)).map=k=[b,0],y=d,f=e.eMarks[o],h=e.sCount[o]+d-(e.bMarks[o]+e.tShift[o]);y<f&&(a=e.src.charCodeAt(y),t(a));)9===a?h+=4-h%4:h++,y++;if(d=y,I=e.tight,c=e.ddIndent,C=e.blkIndent,m=e.tShift[o],g=e.sCount[o],_=e.parentType,e.blkIndent=e.ddIndent=e.sCount[o]+2,e.tShift[o]=d-e.bMarks[o],e.sCount[o]=h,e.tight=!0,e.parentType="deflist",e.md.block.tokenize(e,o,s,!0),e.tight&&!S||(v=!1),S=e.line-o>1&&e.isEmpty(e.line-1),e.tShift[o]=m,e.sCount[o]=g,e.tight=I,e.parentType=_,e.blkIndent=C,e.ddIndent=c,M=e.push("dd_close","dd",-1),k[1]=b=e.line,b>=s)break e;if(e.sCount[b]<e.blkIndent)break e;if((d=n(e,b))<0)break;o=b}if(b>=s)break;if(p=b,e.isEmpty(p))break;if(e.sCount[p]<e.blkIndent)break;if((o=p+1)>=s)break;if(e.isEmpty(o)&&o++,o>=s)break;if(e.sCount[o]<e.blkIndent)break;if((d=n(e,o))<0)break}return M=e.push("dl_close","dl",-1),l[1]=b,e.line=b,v&&function(e,t){var n,r,s=e.level+2;for(n=t+2,r=e.tokens.length-2;n<r;n++)e.tokens[n].level===s&&"paragraph_open"===e.tokens[n].type&&(e.tokens[n+2].hidden=!0,e.tokens[n].hidden=!0,n+=2)}(e,u),!0}),{alt:["paragraph","reference","blockquote"]})}}}]);