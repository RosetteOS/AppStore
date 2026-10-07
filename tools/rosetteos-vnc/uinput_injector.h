#pragma once

#include <cstdint>
#include <string>
#include <vector>

struct EvdevTarget {
    int fd;
    std::string path;
    uint32_t max_x;
    uint32_t max_y;
};

class UinputInjector {
public:
    UinputInjector();
    ~UinputInjector();

    bool init(uint16_t screen_w, uint16_t screen_h);
    void close_device();

    bool is_available() const { return m_uinput_fd >= 0 || !m_evdev_targets.empty(); }

    void inject_pointer(uint16_t x, uint16_t y, uint8_t button_mask);
    void inject_key(uint32_t keysym, bool down);

private:
    int m_uinput_fd;
    std::vector<EvdevTarget> m_evdev_targets;
    uint16_t m_width;
    uint16_t m_height;
    bool m_btn_pressed;
    uint16_t m_last_x;
    uint16_t m_last_y;

    void emit_event(int fd, uint16_t type, uint16_t code, int32_t val);
    void sync_fd(int fd);
    uint16_t keysym_to_keycode(uint32_t keysym);
};

