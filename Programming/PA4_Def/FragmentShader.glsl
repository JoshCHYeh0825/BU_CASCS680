/*

    Fragment shader for PA4

    :author: micou(Zezhou Sun), Daniel Scrivener
    :version: 2025.11.12

*/

#version 330 core

// if you change either of these, make sure you update GLProgram.py!
#define MAX_LIGHT_NUM 20
#define MAX_MATERIAL_NUM 20

struct Material {
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float highlight;
};

struct Light{
    vec3 position;
    vec4 color;
    
    bool infiniteOn;
    vec3 infiniteDirection;
    
    bool spotOn;
    vec3 spotDirection;
    vec3 spotRadialFactor;
    float spotAngleLimit;
};

in vec3 vPos;
in vec3 vColor;
smooth in vec3 vNormal;
in vec2 vTexture;

uniform int renderingFlag;
uniform sampler2D textureImage;

uniform vec3 viewPosition;
uniform Material material;
uniform Light light[MAX_LIGHT_NUM];
uniform vec3 sceneAmbient;

uniform bool imageFlag;
uniform vec3 iResolution;
uniform vec3 iMouse;
uniform float iTime;
out vec4 FragColor;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    ////////// BONUS Course Extra Credit Assignment: SDF visualization and more
    // Requirements:
    //        Implement your advanced rendering techniques in the Fragment shader, 
    //        such as Signed Distance Field (SDF) visualization. Check description for more details.
    vec3 col = vec3(0.0, 0.8, 0.6);
    fragColor = vec4(col,1.0);
}

void main()
{
    if (imageFlag){
        mainImage(FragColor, gl_FragCoord.xy);
        return;
    }

    // These three lines are meaningless, they're just here to prevent GLSL
    // from optimizing out our attributes
    vec4 placeHolder = vec4(vPos+vColor+vNormal+vec3(vTexture, 1), 0);
    FragColor = -1 * abs(placeHolder);
    FragColor = clamp(FragColor, 0, 1);
    
    vec4 results[8];
    for(int i=0; i<8; i+=1)
        results[i]=vec4(0.0);
    int ri=0;
    
    ////////// BONUS 7: Normal Mapping
    // Requirements:
    //   1. Perform the same steps as Texture Mapping above, except that instead of using the image for vertex 
    //   color, the image is used to modify the normals.
    //   2. Use the input normal map ("./assets/normalmap.jpg") on both the sphere and the torus.
    
    // Reserved for illumination rendering, routing name is "lighting" or "illumination"
    if ((renderingFlag >> 0 & 0x1) == 1){
        vec4 result = vec4(vColor, 1.0);

        ////////// TODO 3: Illuminate your meshes
        // Requirements:
        //   Use the illumination equations we learned in the lecture to implement components for Diffuse, 
        //   Specular, and Ambient. You'll implement the missing part in the Fragment shader source code. 
        //   This part will be implemented in OpenGL Shading Language. Your code should iterate through 
        //   all lights in the Light array.

        
        ////////// TODO 4: Set up lights
        // Requirements:
        //   * Use the Light struct which is defined above and the provided Light class to implement 
        //   illumination equations for 3 different light sources: Point light, Infinite light, 
        //   Spotlight with radial and angular attenuation
        //   * In the Sketch.py file Interrupt_keyboard method, bind keyboard interfaces that allows 
        //   the user to toggle on/off specular, diffuse, and ambient with keys S, D, A.

        results[ri] = result;
        ri+=1;
    }
    
    // Reserved for rendering with vertex color, routing name is "vertex"
    if ((renderingFlag >> 1 & 0x1) == 1){
        results[ri] = vec4(vColor, 1.0);
        ri+=1;
    }
    
    // Reserved for rendering with fixed color, routing name is "pure"
    if ((renderingFlag >> 2 & 0x1) == 1){
        results[ri] = vec4(0.5, 0.5, 0.5, 1.0);
        ri+=1;
    }
    
    // Reserved for normal rendering, routing name is "normal"
    if ((renderingFlag >> 3 & 0x1) == 1){
    
        ////////// TODO 2: Set Normal Rendering
        // Requirements:
        //   As a visual debugging mode, you'll implement a rendering mode that visualizes the vertex normals 
        //   with color information. In Fragment Shader, use the vertex normal as the vertex color 
        //   (i.e. the rgb values come from the xyz components of the normal). The value for each dimension in 
        //   vertex normal will be in the range -1 to 1. You will need to offset and rescale them to the 
        //   range 0 to 1.
        
        results[ri] = vec4(0.5, 0.5, 0.5, 1.0);
        ri+=1;
    }
    
    // Reserved for artist rendering, routing name is "artist"
    if ((renderingFlag >> 5 & 0x1) == 1){
        // unused 
        results[ri] = vec4(0.5, 0.5, 0.5, 1.0);
        ri+=1;
    }
    
    // Reserved for some customized rendering, routing name is "custom"
    if ((renderingFlag >> 6 & 0x1) == 1){
        results[ri] = vec4(0.5, 0.5, 0.5, 1.0);
        ri+=1;
    }
    
    // Reserved for texture mapping, get point color from texture image and texture coordinates
    // Routing name is "texture"
    if ((renderingFlag >> 8 & 0x1) == 1){
        results[ri] = texture(textureImage, vTexture);
        ri+=1;
    }
    
    // Mix all results in results array
    vec4 outputResult=vec4(0.0);
    for(int i=0; i<ri; i++){
        outputResult += results[i]/ri;
    }
    FragColor = outputResult;
}