/*

    Vertex shader for PA4

    :author: micou(Zezhou Sun), Daniel Scrivener
    :version: 2025.11.12

*/

#version 330 core
in vec3 aPos;
in vec3 aNormal;
in vec3 aColor;
in vec2 aTexture;

out vec3 vPos;
out vec3 vColor;
smooth out vec3 vNormal;
out vec2 vTexture;
out int materialIndex;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

uniform bool imageFlag;

void main()
{
    if (! imageFlag){
        gl_Position = projection * view * model * vec4(aPos, 1.0);
        vPos = vec3(model * vec4(aPos, 1.0));
        vColor = aColor;
        vNormal = normalize(transpose(inverse(model)) * vec4(aNormal, 0.0) ).xyz;
        vTexture = aTexture;
    }
    else {
        float x = -1.0 + float((gl_VertexID & 1) << 2);
        float y = -1.0 + float((gl_VertexID & 2) << 1);
        gl_Position = vec4(x, y, 0, 1);
    }
}