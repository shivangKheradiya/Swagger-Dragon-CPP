#include <drogon/drogon.h>

using namespace drogon;

int main()
{
    app().setLogPath("./")
         .setLogLevel(trantor::Logger::kWarn)
         .addListener("0.0.0.0", 8848)
         .setThreadNum(8)
         // .enableRunAsDaemon()
         .run();
}