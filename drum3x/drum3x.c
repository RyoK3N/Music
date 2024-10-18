// drum3x.c
// Drum3x - The Ultimate Drum Pad Experience

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_RECORDING_LENGTH 1000  // Max number of beats in a recording

typedef struct {
    int beat_id;
    int timestamp;  // milliseconds since start of recording
} BeatRecord;

static BeatRecord recording[MAX_RECORDING_LENGTH];
static int recording_index = 0;
static int is_recording = 0;
static struct timespec recording_start_time;

void start_recording() {
    recording_index = 0;
    is_recording = 1;
    clock_gettime(CLOCK_MONOTONIC, &recording_start_time);
}

void stop_recording() {
    is_recording = 0;
}

void record_beat(int beat_id) {
    if (!is_recording || recording_index >= MAX_RECORDING_LENGTH) return;
    struct timespec current_time;
    clock_gettime(CLOCK_MONOTONIC, &current_time);
    int timestamp = (current_time.tv_sec - recording_start_time.tv_sec) * 1000
                    + (current_time.tv_nsec - recording_start_time.tv_nsec) / 1000000;
    recording[recording_index].beat_id = beat_id;
    recording[recording_index].timestamp = timestamp;
    recording_index++;
}

int get_recording_length() {
    return recording_index;
}

int get_recorded_beat_id(int index) {
    if (index < 0 || index >= recording_index) return -1;
    return recording[index].beat_id;
}

int get_recorded_beat_timestamp(int index) {
    if (index < 0 || index >= recording_index) return -1;
    return recording[index].timestamp;
}
