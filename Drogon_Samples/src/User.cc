#include "User.h"
#include <drogon/HttpResponse.h>
#include <json/json.h>

using namespace drogon;

namespace api
{
namespace v1
{

void User::getInfo(const HttpRequestPtr &req,
                   std::function<void(const HttpResponsePtr &)> &&callback,
                   int userId) const
{
    Json::Value ret;
    ret["status"] = "ok";
    ret["action"] = "getInfo";
    ret["userId"] = userId;

    auto resp = HttpResponse::newHttpJsonResponse(ret);
    callback(resp);
}

void User::getDetailInfo(const HttpRequestPtr &req,
                         std::function<void(const HttpResponsePtr &)> &&callback,
                         int userId) const
{
    Json::Value ret;
    ret["status"] = "ok";
    ret["action"] = "getDetailInfo";
    ret["userId"] = userId;
    ret["details"] = "This is some detailed info about the user.";

    auto resp = HttpResponse::newHttpJsonResponse(ret);
    callback(resp);
}

void User::newUser(const HttpRequestPtr &req,
                   std::function<void(const HttpResponsePtr &)> &&callback,
                   std::string &&userName)
{
    Json::Value ret;
    ret["status"] = "created";
    ret["action"] = "newUser";
    ret["userName"] = userName;

    auto resp = HttpResponse::newHttpJsonResponse(ret);
    callback(resp);
}

} // namespace v1
} // namespace api