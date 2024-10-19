// drum3x.c
// Drum3x - The Ultimate Drum Pad Experience

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#define EXPORT __declspec(dllexport)
#else
#include <time.h>
#define EXPORT
#endif

#define MAX_RECORDING_LENGTH 1000  // Max number of beats in a recording

typedef struct {
    int beat_id;
    int timestamp;  
} BeatRecord;

static BeatRecord recording[MAX_RECORDING_LENGTH];
static int recording_index = 0;
static int is_recording = 0;

#ifdef _WIN32
static LARGE_INTEGER recording_start_time;
static double frequency_scale;
#else
static struct timespec recording_start_time;
#endif

EXPORT void start_recording() {
    recording_index = 0;
    is_recording = 1;
#ifdef _WIN32
    LARGE_INTEGER frequency;
    QueryPerformanceFrequency(&frequency);
    frequency_scale = 1000.0 / frequency.QuadPart;
    QueryPerformanceCounter(&recording_start_time);
#else
    clock_gettime(CLOCK_MONOTONIC, &recording_start_time);
#endif
}

EXPORT void stop_recording() {
    is_recording = 0;
}

EXPORT void record_beat(int beat_id) {
    if (!is_recording || recording_index >= MAX_RECORDING_LENGTH) return;
#ifdef _WIN32
    LARGE_INTEGER current_time;
    QueryPerformanceCounter(&current_time);
    int timestamp = (int)((current_time.QuadPart - recording_start_time.QuadPart) * frequency_scale);
#else
    struct timespec current_time;
    clock_gettime(CLOCK_MONOTONIC, &current_time);
    int timestamp = (current_time.tv_sec - recording_start_time.tv_sec) * 1000
                    + (current_time.tv_nsec - recording_start_time.tv_nsec) / 1000000;
#endif
    recording[recording_index].beat_id = beat_id;
    recording[recording_index].timestamp = timestamp;
    recording_index++;
}

EXPORT int get_recording_length() {
    return recording_index;
}

EXPORT int get_recorded_beat_id(int index) {
    if (index < 0 || index >= recording_index) return -1;
    return recording[index].beat_id;
}

EXPORT int get_recorded_beat_timestamp(int index) {
    if (index < 0 || index >= recording_index) return -1;
    return recording[index].timestamp;
}
