#include "uinput_injector.h"
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <cstdio>
#include <dirent.h>
#include <sys/ioctl.h>
#include <linux/input.h>
#include <linux/uinput.h>
#include "rfb_protocol.h"

UinputInjector::UinputInjector()
    : m_uinput_fd(-1)
    , m_width(480)
    , m_height(272)
    , m_btn_pressed(false)
    , m_last_x(0)
    , m_last_y(0)
{
}

UinputInjector::~UinputInjector() {
    close_device();
}

bool UinputInjector::init(uint16_t screen_w, uint16_t screen_h) {
    close_device();
    m_width = screen_w;
    m_height = screen_h;

    // 1. Scan and open existing hardware /dev/input/event* devices for direct injection
    for (int i = 0; i < 8; ++i) {
        char path[32];
        std::snprintf(path, sizeof(path), "/dev/input/event%d", i);
        int fd = open(path, O_RDWR | O_NONBLOCK);
        if (fd >= 0) {
            EvdevTarget target;
            target.fd = fd;
            target.path = path;
            target.max_x = 4096; // GuppyScreen EVDEV_CALIBRATE default
            target.max_y = 4096;

            struct input_absinfo abs_x, abs_y;
            if (ioctl(fd, EVIOCGABS(ABS_X), &abs_x) >= 0 && abs_x.maximum > 0) {
                target.max_x = abs_x.maximum;
            } else if (ioctl(fd, EVIOCGABS(ABS_MT_POSITION_X), &abs_x) >= 0 && abs_x.maximum > 0) {
                target.max_x = abs_x.maximum;
            }

            if (ioctl(fd, EVIOCGABS(ABS_Y), &abs_y) >= 0 && abs_y.maximum > 0) {
                target.max_y = abs_y.maximum;
            } else if (ioctl(fd, EVIOCGABS(ABS_MT_POSITION_Y), &abs_y) >= 0 && abs_y.maximum > 0) {
                target.max_y = abs_y.maximum;
            }

            m_evdev_targets.push_back(target);
            fprintf(stdout, "[UinputInjector] Attached direct touch injector to %s (max %ux%u)\n",
                    path, target.max_x, target.max_y);
        }
    }

    // 2. Try uinput virtual device
    const char* uinput_paths[] = { "/dev/uinput", "/dev/input/uinput", nullptr };
    for (int i = 0; uinput_paths[i]; ++i) {
        m_uinput_fd = open(uinput_paths[i], O_WRONLY | O_NONBLOCK);
        if (m_uinput_fd >= 0) break;
    }

    if (m_uinput_fd >= 0) {
        ioctl(m_uinput_fd, UI_SET_EVBIT, EV_KEY);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, BTN_TOUCH);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, BTN_MOUSE);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, BTN_LEFT);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, BTN_RIGHT);

        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_ENTER);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_ESC);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_BACKSPACE);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_TAB);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_SPACE);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_UP);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_DOWN);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_LEFT);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_RIGHT);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_HOME);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_END);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_PAGEUP);
        ioctl(m_uinput_fd, UI_SET_KEYBIT, KEY_PAGEDOWN);

        ioctl(m_uinput_fd, UI_SET_EVBIT, EV_ABS);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_X);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_Y);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_MT_POSITION_X);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_MT_POSITION_Y);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_MT_TRACKING_ID);
        ioctl(m_uinput_fd, UI_SET_ABSBIT, ABS_PRESSURE);

        struct uinput_user_dev uidev;
        std::memset(&uidev, 0, sizeof(uidev));
        std::snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "Rosette VNC Remote Input");
        uidev.id.bustype = BUS_VIRTUAL;
        uidev.id.vendor  = 0x1234;
        uidev.id.product = 0x5678;
        uidev.id.version = 1;

        uidev.absmin[ABS_X] = 0;
        uidev.absmax[ABS_X] = 4096;
        uidev.absmin[ABS_Y] = 0;
        uidev.absmax[ABS_Y] = 4096;
        uidev.absmin[ABS_MT_POSITION_X] = 0;
        uidev.absmax[ABS_MT_POSITION_X] = 4096;
        uidev.absmin[ABS_MT_POSITION_Y] = 0;
        uidev.absmax[ABS_MT_POSITION_Y] = 4096;
        uidev.absmin[ABS_PRESSURE] = 0;
        uidev.absmax[ABS_PRESSURE] = 255;

        if (write(m_uinput_fd, &uidev, sizeof(uidev)) >= 0) {
            if (ioctl(m_uinput_fd, UI_DEV_CREATE) >= 0) {
                fprintf(stdout, "[UinputInjector] Created virtual touch device 'Rosette VNC Remote Input' via uinput\n");
            } else {
                close(m_uinput_fd);
                m_uinput_fd = -1;
            }
        } else {
            close(m_uinput_fd);
            m_uinput_fd = -1;
        }
    }

    if (!is_available()) {
        fprintf(stderr, "[UinputInjector] Notice: No touch injection targets available (view-only mode).\n");
        return false;
    }

    return true;
}

void UinputInjector::close_device() {
    if (m_uinput_fd >= 0) {
        ioctl(m_uinput_fd, UI_DEV_DESTROY);
        close(m_uinput_fd);
        m_uinput_fd = -1;
    }
    for (auto& t : m_evdev_targets) {
        if (t.fd >= 0) {
            close(t.fd);
        }
    }
    m_evdev_targets.clear();
}

void UinputInjector::emit_event(int fd, uint16_t type, uint16_t code, int32_t val) {
    if (fd < 0) return;
    struct input_event ev;
    std::memset(&ev, 0, sizeof(ev));
    ev.type = type;
    ev.code = code;
    ev.value = val;
    ssize_t res = write(fd, &ev, sizeof(ev));
    (void)res;
}

void UinputInjector::sync_fd(int fd) {
    emit_event(fd, EV_SYN, SYN_REPORT, 0);
}

void UinputInjector::inject_pointer(uint16_t x, uint16_t y, uint8_t button_mask) {
    bool pressed = (button_mask & 0x01) != 0;

    // Inject to all evdev devices (e.g. /dev/input/event0)
    for (const auto& target : m_evdev_targets) {
        uint32_t scaled_x = (static_cast<uint32_t>(x) * target.max_x) / (m_width ? m_width : 1);
        uint32_t scaled_y = (static_cast<uint32_t>(y) * target.max_y) / (m_height ? m_height : 1);

        if (pressed) {
            emit_event(target.fd, EV_ABS, ABS_X, scaled_x);
            emit_event(target.fd, EV_ABS, ABS_Y, scaled_y);
            emit_event(target.fd, EV_ABS, ABS_MT_POSITION_X, scaled_x);
            emit_event(target.fd, EV_ABS, ABS_MT_POSITION_Y, scaled_y);
            emit_event(target.fd, EV_ABS, ABS_MT_TRACKING_ID, 0);
            emit_event(target.fd, EV_ABS, ABS_PRESSURE, 200);
            emit_event(target.fd, EV_KEY, BTN_TOUCH, 1);
            emit_event(target.fd, EV_KEY, BTN_MOUSE, 1);
            emit_event(target.fd, EV_KEY, BTN_LEFT, 1);
            sync_fd(target.fd);
        } else if (m_btn_pressed) {
            emit_event(target.fd, EV_ABS, ABS_MT_TRACKING_ID, -1);
            emit_event(target.fd, EV_ABS, ABS_PRESSURE, 0);
            emit_event(target.fd, EV_KEY, BTN_TOUCH, 0);
            emit_event(target.fd, EV_KEY, BTN_MOUSE, 0);
            emit_event(target.fd, EV_KEY, BTN_LEFT, 0);
            sync_fd(target.fd);
        }
    }

    // Inject to uinput virtual device
    if (m_uinput_fd >= 0) {
        uint32_t scaled_x = (static_cast<uint32_t>(x) * 4096) / (m_width ? m_width : 1);
        uint32_t scaled_y = (static_cast<uint32_t>(y) * 4096) / (m_height ? m_height : 1);

        if (pressed) {
            emit_event(m_uinput_fd, EV_ABS, ABS_X, scaled_x);
            emit_event(m_uinput_fd, EV_ABS, ABS_Y, scaled_y);
            emit_event(m_uinput_fd, EV_ABS, ABS_MT_POSITION_X, scaled_x);
            emit_event(m_uinput_fd, EV_ABS, ABS_MT_POSITION_Y, scaled_y);
            emit_event(m_uinput_fd, EV_ABS, ABS_MT_TRACKING_ID, 0);
            emit_event(m_uinput_fd, EV_ABS, ABS_PRESSURE, 200);
            emit_event(m_uinput_fd, EV_KEY, BTN_TOUCH, 1);
            emit_event(m_uinput_fd, EV_KEY, BTN_MOUSE, 1);
            emit_event(m_uinput_fd, EV_KEY, BTN_LEFT, 1);
            sync_fd(m_uinput_fd);
        } else if (m_btn_pressed) {
            emit_event(m_uinput_fd, EV_ABS, ABS_MT_TRACKING_ID, -1);
            emit_event(m_uinput_fd, EV_ABS, ABS_PRESSURE, 0);
            emit_event(m_uinput_fd, EV_KEY, BTN_TOUCH, 0);
            emit_event(m_uinput_fd, EV_KEY, BTN_MOUSE, 0);
            emit_event(m_uinput_fd, EV_KEY, BTN_LEFT, 0);
            sync_fd(m_uinput_fd);
        }
    }

    m_btn_pressed = pressed;
    m_last_x = x;
    m_last_y = y;
}

uint16_t UinputInjector::keysym_to_keycode(uint32_t keysym) {
    switch (keysym) {
        case XK_Return:    return KEY_ENTER;
        case XK_Escape:    return KEY_ESC;
        case XK_BackSpace: return KEY_BACKSPACE;
        case XK_Tab:       return KEY_TAB;
        case XK_Space:     return KEY_SPACE;
        case XK_Up:        return KEY_UP;
        case XK_Down:      return KEY_DOWN;
        case XK_Left:      return KEY_LEFT;
        case XK_Right:     return KEY_RIGHT;
        case XK_Home:      return KEY_HOME;
        case XK_End:       return KEY_END;
        case XK_Page_Up:   return KEY_PAGEUP;
        case XK_Page_Down: return KEY_PAGEDOWN;
        default:           return 0;
    }
}

void UinputInjector::inject_key(uint32_t keysym, bool down) {
    uint16_t code = keysym_to_keycode(keysym);
    if (code == 0) return;

    for (const auto& target : m_evdev_targets) {
        emit_event(target.fd, EV_KEY, code, down ? 1 : 0);
        sync_fd(target.fd);
    }
    if (m_uinput_fd >= 0) {
        emit_event(m_uinput_fd, EV_KEY, code, down ? 1 : 0);
        sync_fd(m_uinput_fd);
    }
}
