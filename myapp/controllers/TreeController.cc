#include "TreeController.h"
#include <drogon/HttpResponse.h>

using namespace drogon;
using drogon_model::myapp::TreeNodes;
using drogon_model::myapp::NodeMetadata;

// ---------------- Helper ----------------
std::pair<std::string, std::function<void(NodeMetadata &)>>
TreeController::detectValue(const Json::Value &v)
{
    if (v.isString())
        return {"value_text", [s = v.asString()](NodeMetadata &m) { m.setValueText(s); }};
    if (v.isBool())
        return {"value_boolean", [b = v.asBool()](NodeMetadata &m) { m.setValueBoolean(b); }};
    if (v.isInt())
        return {"value_int", [i = v.asInt()](NodeMetadata &m) { m.setValueInt(i); }};
    if (v.isDouble()) {
        auto s = std::to_string(v.asDouble());
        return {"value_numeric", [s](NodeMetadata &m) { m.setValueNumeric(s); }};
    }
    return {"value_json", [j = Json::writeString(Json::StreamWriterBuilder(), v)](NodeMetadata &m) {
                m.setValueJson(j);
            }};
}

// ---------------- NODE CRUD ----------------
void TreeController::createNode(const HttpRequestPtr &req,
                                std::function<void(const HttpResponsePtr &)> &&cb)
{
    auto json = req->getJsonObject();
    TreeNodes n;

    if (json && (*json)["parent_id"].isInt())
        n.setParentId((*json)["parent_id"].asInt());

    auto client = app().getDbClient("default");
    Mapper<TreeNodes> mp(client);
    mp.insert(n);

    cb(HttpResponse::newHttpJsonResponse(n.toJson()));
}

void TreeController::getNode(const HttpRequestPtr &req,
                             std::function<void(const HttpResponsePtr &)> &&cb,
                             int nodeId)
{
    auto client = app().getDbClient("default");
    Mapper<TreeNodes> nm(client);
    Mapper<NodeMetadata> mm(client);

    try {
        auto node = nm.findByPrimaryKey(nodeId);
        auto metas = mm.findBy(Criteria(NodeMetadata::Cols::_node_id,
                                       CompareOperator::EQ,
                                       nodeId));

        Json::Value out;
        out["node"] = node.toJson();
        for (auto &m : metas)
            out["metadata"].append(m.toJson());

        cb(HttpResponse::newHttpJsonResponse(out));

    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}

void TreeController::updateNode(const HttpRequestPtr &req,
                                std::function<void(const HttpResponsePtr &)> &&cb,
                                int nodeId)
{
    auto client = app().getDbClient("default");
    Mapper<TreeNodes> nm(client);
    try {
        auto n = nm.findByPrimaryKey(nodeId);
        auto json = req->getJsonObject();

        if (json && (*json)["parent_id"].isInt())
            n.setParentId((*json)["parent_id"].asInt());

        nm.update(n);
        cb(HttpResponse::newHttpJsonResponse(n.toJson()));

    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}

void TreeController::deleteNode(const HttpRequestPtr &req,
                                std::function<void(const HttpResponsePtr &)> &&cb,
                                int nodeId)
{
    auto client = app().getDbClient("default");
    Mapper<TreeNodes> nm(client);
    try {
        nm.deleteByPrimaryKey(nodeId);
        cb(HttpResponse::newHttpResponse());

    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}

// ---------------- METADATA CRUD ----------------
void TreeController::addMetadata(const HttpRequestPtr &req,
                                 std::function<void(const HttpResponsePtr &)> &&cb,
                                 int nodeId)
{
    auto json = req->getJsonObject();

    if (!json || !json->isMember("key_name") || !json->isMember("value")) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k400BadRequest);
        cb(r);
        return;
    }

    auto client = app().getDbClient("default");
    Mapper<NodeMetadata> mm(client);

    NodeMetadata m;
    m.setNodeId(nodeId);
    m.setKeyName((*json)["key_name"].asString());

    auto [col, setter] = detectValue((*json)["value"]);
    setter(m);

    mm.insert(m);
    cb(HttpResponse::newHttpJsonResponse(m.toJson()));
}

void TreeController::updateMetadata(const HttpRequestPtr &req,
                                    std::function<void(const HttpResponsePtr &)> &&cb,
                                    int metadataId)
{
    auto client = app().getDbClient("default");
    Mapper<NodeMetadata> mm(client);

    try {
        auto m = mm.findByPrimaryKey(metadataId);
        auto json = req->getJsonObject();

        if (!json || !json->isMember("value")) {
            auto r = HttpResponse::newHttpResponse();
            r->setStatusCode(k400BadRequest);
            cb(r);
            return;
        }

        auto [col, setter] = detectValue((*json)["value"]);
        setter(m);

        mm.update(m);
        cb(HttpResponse::newHttpJsonResponse(m.toJson()));

    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}

void TreeController::deleteMetadata(const HttpRequestPtr &req,
                                    std::function<void(const HttpResponsePtr &)> &&cb,
                                    int metadataId)
{
    auto client = app().getDbClient("default");
    Mapper<NodeMetadata> mm(client);

    try {
        mm.deleteByPrimaryKey(metadataId);
        cb(HttpResponse::newHttpResponse());

    } catch (...) {
        auto r = HttpResponse::newHttpResponse();
        r->setStatusCode(k404NotFound);
        cb(r);
    }
}
