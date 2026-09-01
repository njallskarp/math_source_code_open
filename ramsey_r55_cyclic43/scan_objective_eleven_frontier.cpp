#define main objective_six_component_embedded_main
#include "objective_six_component.cpp"
#undef main

int main(int argc, char** argv) try {
    if (argc != 9) {
        std::cerr
            << "usage: scan_objective_eleven_frontier CERTIFICATE.json "
               "LOWER-SIX.json OBJECTIVE-SEVEN-COMPONENT.json "
               "OBJECTIVE-EIGHT-COMPONENT.json OBJECTIVE-NINE-COMPONENT.json "
               "OBJECTIVE-TEN-FRONTIER.json OBJECTIVE-TEN-COMPONENT.json "
               "OUTPUT.json\n";
        return 2;
    }
    Search search(load_flips(argv[1]));
    search.write_objective_eleven_frontier_from_certificates(
        argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8]
    );
    return 0;
} catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
