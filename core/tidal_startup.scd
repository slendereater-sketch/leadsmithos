(
s.reconfig;
s.options.numBuffers = 1024 * 512; // Z2A Master Optimization
s.options.memSize = 8192 * 128;   // High-Density Memory Allocation
s.options.blockSize = 64;        // Ultra-Low Latency
s.options.sampleRate = 48000;
s.options.numOutputBusChannels = 2;
s.options.numInputBusChannels = 2;
s.waitForBoot {
    ~dirt = SuperDirt(2, s);
    ~dirt.loadSoundFiles;
    s.sync;
    ~dirt.start(57120, [0, 0]);
    "LEADSMITH Z2A AUDIO ENGINE: IGNITED AT 120Hz PRIORITY".postln;
};
);
