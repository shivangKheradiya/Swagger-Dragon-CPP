
// [ADDED] SwaggerController.h - serves /api-docs (OpenAPI JSON) and /swagger (Swagger UI)
#pragma once
#include <drogon/HttpController.h>

class SwaggerController : public drogon::HttpController<SwaggerController> {
public:
    METHOD_LIST_BEGIN
    // [ADDED] Expose OpenAPI spec as JSON at /api-docs
    METHOD_ADD(SwaggerController::getDocs, "/api-docs", drogon::Get);
    // [ADDED] Serve a minimal Swagger UI page at /swagger
    METHOD_ADD(SwaggerController::swaggerUI, "/swagger", drogon::Get);
    METHOD_LIST_END

    void getDocs(const drogon::HttpRequestPtr& req,
                 std::function<void(const drogon::HttpResponsePtr&)>&& cb) const;
    void swaggerUI(const drogon::HttpRequestPtr& req,
                   std::function<void(const drogon::HttpResponsePtr&)>&& cb) const;
};
