
#pragma once
#include <drogon/HttpController.h>

class UsersController : public drogon::HttpController<UsersController> {
public:
    METHOD_LIST_BEGIN
    ADD_METHOD_TO(UsersController::listUsers, "/users", drogon::Get);
    ADD_METHOD_TO(UsersController::getUser, "/users/{1}", drogon::Get);
    ADD_METHOD_TO(UsersController::createUser, "/users", drogon::Post);
    METHOD_LIST_END

    void listUsers(const drogon::HttpRequestPtr&,
                   std::function<void(const drogon::HttpResponsePtr&)>&& cb);
    /**
    * @brief Get all users
    * @path /users
    * @method GET
    * @response 200 json Returns a list of users
    */
    void getUser(const drogon::HttpRequestPtr&,
                 std::function<void(const drogon::HttpResponsePtr&)>&& cb,
                 int id);

    void createUser(const drogon::HttpRequestPtr&,
                    std::function<void(const drogon::HttpResponsePtr&)>&& cb);
};
