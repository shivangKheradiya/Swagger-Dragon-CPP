
    // [ADDED] SwaggerController.cc - implements Swagger UI + OpenAPI JSON
    #include "SwaggerController.h"
    #include <drogon/HttpResponse.h>
    #include <json/json.h>

    using drogon::HttpRequestPtr;
    using drogon::HttpResponse;
    using drogon::HttpResponsePtr;

    void SwaggerController::getDocs(const HttpRequestPtr& req,
                                    std::function<void(const HttpResponsePtr&)>&& cb) const {
        // [ADDED] Minimal OpenAPI 3.0 spec describing Users resources based on your model
        Json::Value openapi;
        openapi["openapi"] = "3.0.3"; // [ADDED]
        openapi["info"]["title"] = "MyApp API"; // [ADDED]
        openapi["info"]["version"] = "1.0.0"; // [ADDED]
        openapi["servers"][0]["url"] = "/"; // [ADDED]

        // [ADDED] Schemas
        Json::Value schemas;
        Json::Value user;
        user["type"] = "object";
        user["properties"]["id"]["type"] = "integer";
        user["properties"]["username"]["type"] = "string";
        user["properties"]["email"]["type"] = "string";
        user["properties"]["password_hash"]["type"] = "string";
        user["properties"]["created_at"]["type"] = "string";
        user["properties"]["created_at"]["format"] = "date-time";
        schemas["User"] = user;

        Json::Value userCreate = user; // [ADDED]
        // [ADDED] For creation, id and created_at are server managed
        userCreate["required"] = Json::arrayValue;
        userCreate["required"].append("username");
        userCreate["required"].append("email");
        userCreate["required"].append("password_hash");
        userCreate["properties"].removeMember("id");
        userCreate["properties"].removeMember("created_at");
        schemas["UserCreate"] = userCreate;

        openapi["components"]["schemas"] = schemas;

        // [ADDED] Paths
        Json::Value paths;

        // GET /users
        {
            Json::Value getOp;
            getOp["summary"] = "List users";
            getOp["responses"]["200"]["description"] = "OK";
            getOp["responses"]["200"]["content"]["application/json"]["schema"]["type"] = "array";
            getOp["responses"]["200"]["content"]["application/json"]["schema"]["items"]["$ref"] = "#/components/schemas/User";
            paths["/users"]["get"] = getOp;
        }
        // POST /users
        {
            Json::Value postOp;
            postOp["summary"] = "Create a user";
            postOp["requestBody"]["required"] = true;
            postOp["requestBody"]["content"]["application/json"]["schema"]["$ref"] = "#/components/schemas/UserCreate";
            postOp["responses"]["201"]["description"] = "Created";
            postOp["responses"]["201"]["content"]["application/json"]["schema"]["$ref"] = "#/components/schemas/User";
            paths["/users"]["post"] = postOp;
        }
        // GET /users/{id}
        {
            Json::Value getById;
            getById["summary"] = "Get user by id";
            getById["parameters"][0]["name"] = "id";
            getById["parameters"][0]["in"] = "path";
            getById["parameters"][0]["required"] = true;
            getById["parameters"][0]["schema"]["type"] = "integer";
            getById["responses"]["200"]["description"] = "OK";
            getById["responses"]["200"]["content"]["application/json"]["schema"]["$ref"] = "#/components/schemas/User";
            getById["responses"]["404"]["description"] = "Not Found";
            paths["/users/{id}"]["get"] = getById;
        }

        openapi["paths"] = paths;

        auto resp = HttpResponse::newHttpJsonResponse(openapi);
        // [ADDED] Allow Swagger UI from other origins if needed
        resp->addHeader("Access-Control-Allow-Origin", "*");
        cb(resp);
    }

    void SwaggerController::swaggerUI(const HttpRequestPtr& req,
                                      std::function<void(const HttpResponsePtr&)>&& cb) const {
        // [ADDED] Serve a tiny HTML that loads Swagger UI from CDN and points it to /api-docs
        static const char* kHtml = R"HTML(
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: '/api-docs',
        dom_id: '#swagger-ui',
        presets: [SwaggerUIBundle.presets.apis],
        layout: 'BaseLayout'
      });
    </script>
  </body>
</html>)HTML";
        auto resp = HttpResponse::newHttpResponse();
        resp->setStatusCode(drogon::k200OK);
        resp->setContentTypeCode(drogon::CT_TEXT_HTML);
        resp->setBody(kHtml);
        cb(resp);
    }
