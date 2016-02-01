# version 130

// uniform vec3 glowColor;
varying float intensity;

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

// Output to fragment shader
out vec2 texcoord;

void main()
{
    vec3 glowColor = vec3(1.0, 0.5, 0.5);
	vec3 glow = glowColor * intensity;
    gl_FragColor = vec4( glow, 1.0 );
}
