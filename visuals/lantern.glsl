#define FIELD sTD2DInputs[0]
uniform vec4 uTile;
uniform vec3 uCentre, uRight, uUp, uSight;
uniform vec4 uSettings;
#define uFrame uSettings.x
#define uAspect uSettings.y
#define uExposure uSettings.z
#define uScale uSettings.w
const float uWeight=1.;
const int uNeutral=0, uMask=3, uMode=1;
const float uThickness=1.;
const int uCut=1, uSecond=-1;
const float extent=2.22;
const int COUNT=8; const float ratio=0.41421356237310;
const mat3 Q[COUNT]=mat3[COUNT](mat3(vec3(0.659739608441,-0.726726906549,-0.191341716183),vec3(0.592752310333,0.659739608441,-0.461939766256),vec3(0.461939766256,0.191341716183,0.866025403784)),mat3(vec3(0.726726906549,-0.659739608441,0.191341716183),vec3(0.659739608441,0.592752310333,-0.461939766256),vec3(0.191341716183,0.461939766256,0.866025403784)),mat3(vec3(0.659739608441,-0.592752310333,0.461939766256),vec3(0.726726906549,0.659739608441,-0.191341716183),vec3(-0.191341716183,0.461939766256,0.866025403784)),mat3(vec3(0.592752310333,-0.659739608441,0.461939766256),vec3(0.659739608441,0.726726906549,0.191341716183),vec3(-0.461939766256,0.191341716183,0.866025403784)),mat3(vec3(0.659739608441,-0.726726906549,0.191341716183),vec3(0.592752310333,0.659739608441,0.461939766256),vec3(-0.461939766256,-0.191341716183,0.866025403784)),mat3(vec3(0.726726906549,-0.659739608441,-0.191341716183),vec3(0.659739608441,0.592752310333,0.461939766256),vec3(-0.191341716183,-0.461939766256,0.866025403784)),mat3(vec3(0.659739608441,-0.592752310333,-0.461939766256),vec3(0.726726906549,0.659739608441,0.191341716183),vec3(0.191341716183,-0.461939766256,0.866025403784)),mat3(vec3(0.592752310333,-0.659739608441,-0.461939766256),vec3(0.659739608441,0.726726906549,-0.191341716183),vec3(0.461939766256,-0.191341716183,0.866025403784)));
const vec3 T[COUNT]=vec3[COUNT](vec3(1.277580409184,0.529191132506,0.139332035968),vec3(0.529191132506,1.277580409184,0.139332035968),vec3(-0.529191132506,1.277580409184,0.139332035968),vec3(-1.277580409184,0.529191132506,0.139332035968),vec3(-1.277580409184,-0.529191132506,0.139332035968),vec3(-0.529191132506,-1.277580409184,0.139332035968),vec3(0.529191132506,-1.277580409184,0.139332035968),vec3(1.277580409184,-0.529191132506,0.139332035968));
vec2 field(vec3 pos) {
    vec3 g = clamp((pos + extent)*(95./(2.*extent)), 0., 95.);
    float k = floor(g.z);
    vec2 a = vec2(mod(k,12.),floor(k/12.))*96.;
    float next = min(k+1.,95.);
    vec2 b = vec2(mod(next,12.),floor(next/12.))*96.;
    vec2 uv = g.xy+.5;
    vec2 atlas = vec2(1152.,768.);
    vec2 value = mix(textureLod(FIELD, vec2(((a+uv)/atlas).x, 1.-((a+uv)/atlas).y), 0.).rg,
                     textureLod(FIELD, vec2(((b+uv)/atlas).x, 1.-((b+uv)/atlas).y), 0.).rg, fract(g.z));
    return vec2(value.r*.8, value.g);
}

struct Hit {
    float depth;
    vec3 local;
    mat3 rotation;
    float scale;
    vec3 color;
    ivec4 address;
};

// Test bounded copies independently. All keep their actual positions even
// when the camera follows the repeated address 000.
void traceCopy(vec3 origin, vec3 ray, vec3 centre, mat3 rotation, float scale,
               ivec4 address, float skin, inout Hit hit) {
    vec3 rel = origin-centre;
    float mid = -dot(rel,ray);
    vec3 side = rel+mid*ray;
    float disc = ((2.14+skin)*scale)*((2.14+skin)*scale)-dot(side,side);
    if (disc<=0.) return;
    float radius = sqrt(disc);
    float start = max(0.,mid-radius);
    if (start>=hit.depth) return;
    float end = (min(mid+radius,hit.depth)-start)/scale;
    mat3 inverseQ = transpose(rotation);
    vec3 from = inverseQ*(rel+ray*start)/scale;
    vec3 direction = inverseQ*ray;
    float travel = 0.;
    for (int step=0; step<88; ++step) {
        if (travel>=end) break;
        vec3 p = from + direction*travel;
        float d = field(p).x-skin;
        if(uCut!=0 && address.x<2){
            vec3 world=centre+scale*rotation*p;
            float signCut=address.x==0 ? -1. : 1.;
            if(uCut==2)signCut=-signCut;
            float cut=signCut*(world.x-world.y)*.7071067811865475/scale;
            d=max(d,cut);
        }
        if (d<.0018) {
            hit = Hit(start+scale*travel,p,rotation,scale,vec3(0),address);
            return;
        }
        travel += max(.0015, .86*d);
    }
}

vec3 normalAt(vec3 p) {
    const vec2 e = vec2(.021,-.021);
    vec3 n = e.xyy*field(p+e.xyy).x + e.yyx*field(p+e.yyx).x
           + e.yxy*field(p+e.yxy).x + e.xxx*field(p+e.xxx).x;
    return n/max(length(n),.00001);
}

float shadow(vec3 pos, vec3 light) {
    // The parent atlas provides soft contact shadows over the whole assembly.
    float t=.085, visibility=1.;
    for (int i=0; i<18; ++i) {
        vec3 p = pos+t*light;
        if (length(p)>2.22 || t>2.9) break;
        float d = field(p).x;
        visibility = min(visibility, (d+.008)*9./t);
        t += clamp(d*.9,.045,.32);
    }
    return clamp(visibility,.12,1.);
}

Hit traceScene(vec3 origin,vec3 ray,float skin){Hit hit=Hit(16.,vec3(0),mat3(1),1.,vec3(0),ivec4(0));
for(int i=0;i<COUNT;++i){if((uMask & (1<<i))==0)continue;vec3 p1=T[i];mat3 q1=Q[i];float r1=ratio;vec3 delta=p1-origin;float mid=dot(delta,ray);float rad=2.40*r1;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
for(int j=0;j<COUNT;++j){if(uSecond>=0 && j!=uSecond)continue;vec3 p2=p1+r1*q1*T[j];mat3 q2=q1*Q[j];float r2=r1*ratio;vec3 delta=p2-origin;float mid=dot(delta,ray);float rad=2.40*r2;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
for(int k=0;k<COUNT;++k){vec3 p3=p2+r2*q2*T[k];mat3 q3=q2*Q[k];float r3=r2*ratio;vec3 delta=p3-origin;float mid=dot(delta,ray);float rad=2.40*r3;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
for(int l=0;l<COUNT;++l){vec3 p4=p3+r3*q3*T[l];mat3 q4=q3*Q[l];float r4=r3*ratio;vec3 delta=p4-origin;float mid=dot(delta,ray);float rad=2.40*r4;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
for(int m=0;m<COUNT;++m){vec3 p5=p4+r4*q4*T[m];mat3 q5=q4*Q[m];float r5=r4*ratio;vec3 delta=p5-origin;float mid=dot(delta,ray);float rad=2.40*r5;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
for(int n=0;n<COUNT;++n){vec3 p6=p5+r5*q5*T[n];mat3 q6=q5*Q[n];float r6=r5*ratio;vec3 delta=p6-origin;float mid=dot(delta,ray);float rad=2.40*r6;if(mid+rad<0. || mid-rad>hit.depth || dot(delta,delta)-mid*mid>rad*rad)continue;
traceCopy(origin,ray,p6,q6,r6,ivec4(i,j,k,l),skin,hit);}}}}}}return hit;}
// Surface, directional density shading, soft shadow, satin highlights and
// tone mapping adapted directly from sixfold/sculpture.frag's metal study.
vec4 render(vec2 uv){
    vec2 plane=(uv-.5)*vec2(uAspect,1.);
    vec3 ray=-uSight;
    vec3 origin=uCentre+uFrame*(uRight*plane.x+uUp*plane.y)+uSight*6.;
    float skin=clamp(.005*uScale*uThickness/0.00505063388335,.012,.24);
    Hit hit=traceScene(origin,ray,skin);
    vec2 vignette=(uv-vec2(.44,.54))*vec2(1.22,1.);
    vec3 bg=mix(vec3(.008,.014,.023),vec3(.066,.108,.122),exp(-6.5*dot(vignette,vignette)));
    if(hit.depth>15.){return vec4(bg,1.);}
    vec3 point=origin+hit.depth*ray;
    vec3 copper=vec3(.94,.40,.105),teal=vec3(.026,.46,.41);
    vec3 steel=vec3(.22,.33,.39);
    vec3 material[8]=vec3[8](copper,steel,teal,steel,copper,steel,teal,steel);
    float descent=log(uScale)/log(ratio);
    vec3 albedo=mix(material[hit.address.x],material[hit.address.y],.13+.72*smoothstep(.45,1.5,descent));
    albedo=mix(albedo,material[hit.address.z],.065+.62*smoothstep(1.55,2.6,descent));
    if(4==4)albedo=mix(albedo,material[hit.address.w],.04+.30*smoothstep(2.40,3.,descent));
    if(uNeutral==1)albedo=vec3(.55,.59,.60);
    vec3 diagnostic[8]=vec3[8](vec3(0.94,0.4,0.105),vec3(0.04,0.57,0.49),vec3(0.32,0.47,0.83),vec3(0.78,0.3,0.42),vec3(0.72,0.63,0.24),vec3(0.43,0.66,0.3),vec3(0.58,0.35,0.74),vec3(0.2,0.62,0.75));
if(uMode==1)albedo=hit.address.x<2 ? diagnostic[hit.address.x] : vec3(.38,.43,.46);if(uMode==2)albedo=vec3(.56,.61,.60);
if(uMode==3)albedo=point.x>=point.y ? vec3(.94,.40,.105) : vec3(.04,.57,.49);
    vec3 n=hit.rotation*normalAt(hit.local);
    if(uCut!=0 && hit.address.x<2){
        float signCut=hit.address.x==0 ? -1. : 1.;
        if(uCut==2)signCut=-signCut;
        float cut=signCut*(point.x-point.y)*.7071067811865475/hit.scale;
        if(cut>field(hit.local).x-skin) n=signCut*vec3(.7071067811865475,-.7071067811865475,0.);
    }
    vec3 key=normalize(-.75*uRight+.94*uUp+.26*uSight);
    vec3 fill=normalize(.80*uRight+.28*uUp+.17*uSight);
    vec3 loc=point,keyLocal=key;
    float density=0.,slope=0.;
    for(int level=0;level<4;++level){
        float front=field(loc+.20*keyLocal).y;
        float behind=field(loc-.20*keyLocal).y;
        slope+=behind-front;density+=front;
        int digit=hit.address[level];
        loc=transpose(Q[digit])*(loc-T[digit])/ratio;
        keyLocal=transpose(Q[digit])*keyLocal;
    }
    float mask=shadow(point,key);
    float ndl=max(0.,dot(n,key));
    float ao=exp(-.85*density);
    float broadLight=clamp(.47+.35*slope,.07,1.15);
    vec3 halfKey=normalize(key+uSight);
    float spec=pow(max(dot(n,halfKey),0.),14.);
    float rim=pow(1.-clamp(dot(n,uSight),0.,1.),2.4);
    vec3 reflected=albedo*(vec3(.043,.09,.13)+(.18+.95*ndl)*vec3(1.36,1.04,.66)*broadLight*(.19+.81*mask)
        +.22*max(0.,dot(n,fill))*vec3(.30,.69,1.))*ao;
    reflected+=mask*broadLight*ao*spec*mix(vec3(.85,.76,.57),albedo,.45)*.53;
    reflected+=rim*(.023+.16*max(0.,dot(n,fill)))*vec3(.24,.62,.86)*ao;
    float relief=dot(point-uCentre,uSight)/max(uScale,.26);
    reflected*=uExposure*clamp(.90+.26*relief,.50,1.35);
    vec3 color=pow(clamp(1.-exp(-1.35*reflected),0.,1.),vec3(.4545));
    return vec4(color,1.);
}

layout(location=0) out vec4 fragColor;
void main(){fragColor=TDOutputSwizzle(render(uTile.xy+vUV.st*uTile.zw));}
