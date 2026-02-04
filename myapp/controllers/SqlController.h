#pragma once
#include <drogon/HttpController.h>
#include <drogon/orm/DbClient.h>
#include <json/json.h>

class SqlController : public drogon::HttpController<SqlController>
{
  public:
    METHOD_LIST_BEGIN
    // POST /sql
    ADD_METHOD_TO(SqlController::runSql, "/sql", drogon::Post);
    // Optionally require auth filter:
    // ADD_METHOD_TO(SqlController::runSql, "/sql", drogon::Post, "AuthFilter");
    METHOD_LIST_END

    // Handler
    void runSql(const drogon::HttpRequestPtr &req,
                std::function<void (const drogon::HttpResponsePtr &)> &&callback) const;

  private:
    // Helper: convert Drogon SQL result set to JSON array
    static Json::Value resultToJson(const drogon::orm::Result &r);

    // Helper: detect if query starts with SELECT / WITH to decide response shape
    static bool isSelectLike(const std::string &query);
};