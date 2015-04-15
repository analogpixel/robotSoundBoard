Gain master => Pan2 pan => dac;

SinOsc s => master;
SndBuf2 s1 => master;

.05 => s.gain;
2.2 => s1.gain;

me.dir() + "out.wav" => s1.read;
s1.samples() => s1.pos;

now => time start;
0 => s1.pos;

while ( start + 2::second > now) {
			Math.random2f(100,600) => s.freq;
			50::ms => now;
    
}
