#version 130

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

// Output to fragment shader
out vec2 texcoord;

void main(void) {
    vec4 a = p3d_Vertex;
//    a.x *= 0.5;
//    a.y *= 0.5;
//    a.z *= 0.5;

    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;
    texcoord.x += float(int((p3d_Vertex.x) * 1000) % 1000) / 1000;
    texcoord.y += float(int((p3d_Vertex.y) * 1000) % 1000) / 1000;
//    texcoord.xy+= float(int(p3d_Vertex.y + p3d_Vertex.z * 1000) / 1000;
//    texcoord.y = texcoord.x;

//    texcoord.y += p3d_Vertex.y / 10;

//    texcoord = p3d_MultiTexCoord0;
//    gl_Vertex.x += 0.01;
}
