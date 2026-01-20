/// The header file
#pragma once
#include <drogon/HttpSimpleController.h>
#include <json/json.h>

using namespace drogon;

class JsonCtrl : public drogon::HttpSimpleController<JsonCtrl>
{
  public:
    void asyncHandleHttpRequest(const HttpRequestPtr &req, std::function<void(const HttpResponsePtr &)> &&callback) override;
    PATH_LIST_BEGIN
    //list path definitions here;
    PATH_ADD("/json", Get);
    PATH_LIST_END
};