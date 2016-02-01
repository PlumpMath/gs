#version 130

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

void main(void) {
//    gl_FragColor = vec4(0.0. 1.0, 0.0, 1.0);
//    texcoord.x *= 2;
//    gl_FragColor = texture2D(p3d_Texture0, texcoord);
//    gl_FragColor = vec4(0, 0.5, 0, 1);

//    vec2 c = texcoord;
//    c.x *= 2;
    vec4 color = texture(p3d_Texture0, texcoord);
    gl_FragColor = color.rgba;
}
