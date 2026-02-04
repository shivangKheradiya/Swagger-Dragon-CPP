#include "SqlController.h"
#include <algorithm>
#include <cctype>
#include <string>

using drogon::HttpResponse;
using drogon::HttpResponsePtr;
using drogon::HttpRequestPtr;
using drogon::orm::DrogonDbException;
using drogon::orm::Result;

namespace
{
    // Trim leading whitespace (simple helper)
    std::string ltrim(std::string s) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
            return !std::isspace(ch);
        }));
        return s;
    }

    // Uppercase the first token (word) in the SQL string
    std::string firstWordUpper(std::string sql) {
        sql = ltrim(std::move(sql));
        std::string w;
        for (char c : sql) {
            if (std::isspace(static_cast<unsigned char>(c))) break;
            w.push_back(static_cast<char>(std::toupper(static_cast<unsigned char>(c))));
        }
        return w;
    }
}

Json::Value SqlController::resultToJson(const Result &r)
{
    Json::Value arr(Json::arrayValue);
    for (const auto &row : r)
    {
        Json::Value obj(Json::objectValue);
        for (size_t i = 0; i < r.columns(); ++i)
        {
            const auto &colName = r.columnName(i);
            const auto &field = row[i];
            if (field.isNull())
            {
                obj[colName] = Json::nullValue;
            }
            else
            {
                // Keep it simple/portable: everything as string
                // If you want typed JSON, map by column types and call as<int>(), as<double>(), etc.
                obj[colName] = field.as<std::string>();
            }
        }
        arr.append(std::move(obj));
    }
    return arr;
}

bool SqlController::isSelectLike(const std::string &query)
{
    auto first = firstWordUpper(query);
    return (first == "SELECT" || first == "WITH" || first == "SHOW" || first == "DESCRIBE");
}

void SqlController::runSql(const HttpRequestPtr &req,
                           std::function<void (const HttpResponsePtr &)> &&callback) const
{
    auto json = req->getJsonObject();
    if (!json || !json->isMember("query"))
    {
        Json::Value out(Json::objectValue);
        out["rows"] = Json::arrayValue;
        out["affectedRows"] = 0;
        out["error"] = "Missing 'query' in JSON body";
        auto resp = HttpResponse::newHttpJsonResponse(out);
        resp->setStatusCode(drogon::k400BadRequest);
        return callback(resp);
    }

    // Read query
    const std::string query = (*json)["query"].asString();

    // 🔐 Optional soft guard (you can remove/adjust):
    // Disallow obvious destructive statements unless you really want to allow them.
    // if (firstWordUpper(query) == "DROP" || firstWordUpper(query) == "TRUNCATE") { ... }

    // If you want to add parameter support, you can extend here:
    // Example expected body:
    // { "query": "SELECT * FROM users WHERE id=$1", "params": [123] }
    // See notes at the end of this file for a param-enabled variant.

    auto dbClient = drogon::app().getDbClient();

    // Execute asynchronously
    dbClient->execSqlAsync(
        query,
        // Success callback
        [callback, query](const Result &r) {
            Json::Value out(Json::objectValue);
            if (isSelectLike(query))
            {
                out["rows"] = resultToJson(r);
                out["affectedRows"] = 0;
            }
            else
            {
                out["rows"] = Json::arrayValue;
                out["affectedRows"] = static_cast<Json::UInt64>(r.affectedRows());
            }
            out["error"] = Json::nullValue;

            auto resp = HttpResponse::newHttpJsonResponse(out);
            callback(resp);
        },
        // Error callback
        [callback](const DrogonDbException &e) {
            Json::Value out(Json::objectValue);
            out["rows"] = Json::arrayValue;
            out["affectedRows"] = 0;
            out["error"] = e.base().what();

            auto resp = HttpResponse::newHttpJsonResponse(out);
            resp->setStatusCode(drogon::k400BadRequest);
            callback(resp);
        }
        // NOTE: No parameters passed here for simplicity.
        // For parameterized queries, use the overload with a parameters array/vector.
    );
}

/*
==========================================================
Notes: Adding Prepared Parameters (if/when you need them)
==========================================================
If you want to support parameters now, update runSql() to read a JSON "params" array
and pass it to the appropriate execSqlAsync overload. Example body:

{
  "query": "SELECT * FROM users WHERE id=$1 AND active=$2",
  "params": [123, true]
}

Two approaches:

1) Using execSqlAsyncFuture (C++17) with type-erased VariantArray (varargs friendly):
   - Convert JSON params into a drogon::orm::VariantArray (std::vector<trantor::any>).
   - Then call client->execSqlAsyncFuture(query, variantArray);

2) Using the execSqlAsync overload that accepts parameter collections (supported by Drogon).
   - Construct a vector of drogon::orm::Parameter types or raw buffers per your DB.

For portability and simplicity, many teams start without params and migrate to a whitelisted,
named-operations approach (e.g., { "op": "get_user", "args": { "id": 123 } }).
If you want, I can wire this for you with typed params + validation.
*/
