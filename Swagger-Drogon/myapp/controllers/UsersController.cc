
#include "UsersController.h"
#include <drogon/HttpResponse.h>
#include <drogon/drogon.h>
#include <models/Users.h>
#include <drogon/orm/Mapper.h>

using namespace drogon;
using drogon_model::myapp::Users;

void UsersController::listUsers(const HttpRequestPtr&,    std::function<void(const HttpResponsePtr&)>&& cb) {
    auto client = app().getDbClient("default");
    orm::Mapper<Users> mp(client);
    auto all = mp.findAll();

    Json::Value arr(Json::arrayValue);
    for (auto &u : all) arr.append(u.toJson());

    cb(HttpResponse::newHttpJsonResponse(arr));
}

void UsersController::getUser(const HttpRequestPtr&,    std::function<void(const HttpResponsePtr&)>&& cb, int id) {
    auto client = app().getDbClient("default");
    orm::Mapper<Users> mp(client);
    try {
        auto u = mp.findByPrimaryKey(id);
        cb(HttpResponse::newHttpJsonResponse(u.toJson()));
    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}


void UsersController::createUser(
    const drogon::HttpRequestPtr& req,
    std::function<void(const drogon::HttpResponsePtr&)>&& cb) {

    auto json = req->getJsonObject();
    if (!json) {
        auto r = drogon::HttpResponse::newHttpResponse();
        r->setStatusCode(drogon::k400BadRequest);
        cb(r);
        return;
    }

    // Build from JSON and set created_at
    drogon_model::myapp::Users u(*json);
    u.setCreatedAt(trantor::Date::now());

    auto client = drogon::app().getDbClient("default");
    drogon::orm::Mapper<drogon_model::myapp::Users> mp(client);

    // NOTE: When 'insert' returns void (e.g. MySQL/SQLite), this compiles fine.
    mp.insert(u);

    // If your DB/driver doesn’t fill the ID back into 'u', it may be missing here.
    auto r = drogon::HttpResponse::newHttpJsonResponse(u.toJson());
    r->setStatusCode(drogon::k201Created);
    cb(r);
}
