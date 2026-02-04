#pragma once
#include <drogon/HttpController.h>
#include <drogon/orm/Mapper.h>
#include <drogon/drogon.h>
#include <models/TreeNodes.h>
#include <models/NodeMetadata.h>

using namespace drogon;
using namespace drogon::orm;
using drogon_model::myapp::TreeNodes;
using drogon_model::myapp::NodeMetadata;

class TreeController : public HttpController<TreeController>
{
public:
    METHOD_LIST_BEGIN
        // Node CRUD
        ADD_METHOD_TO(TreeController::createNode, "/nodes", Post);
        ADD_METHOD_TO(TreeController::getNode, "/nodes/{1}", Get);
        ADD_METHOD_TO(TreeController::updateNode, "/nodes/{1}", Put);
        ADD_METHOD_TO(TreeController::deleteNode, "/nodes/{1}", Delete);

        // Metadata CRUD (single only, no bulk)
        ADD_METHOD_TO(TreeController::addMetadata, "/nodes/{1}/metadata", Post);
        ADD_METHOD_TO(TreeController::updateMetadata, "/metadata/{1}", Put);
        ADD_METHOD_TO(TreeController::deleteMetadata, "/metadata/{1}", Delete);
    METHOD_LIST_END

    // Node CRUD
    void createNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb);

    void getNode(const HttpRequestPtr &req,
                 std::function<void(const HttpResponsePtr &)> &&cb,
                 int nodeId);

    void updateNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb,
                    int nodeId);

    void deleteNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb,
                    int nodeId);

    // Metadata CRUD
    void addMetadata(const HttpRequestPtr &req,
                     std::function<void(const HttpResponsePtr &)> &&cb,
                     int nodeId);

    void updateMetadata(const HttpRequestPtr &req,
                        std::function<void(const HttpResponsePtr &)> &&cb,
                        int metadataId);

    void deleteMetadata(const HttpRequestPtr &req,
                        std::function<void(const HttpResponsePtr &)> &&cb,
                        int metadataId);

private:
    std::pair<std::string, std::function<void(NodeMetadata &)>>
    detectValue(const Json::Value &value);
};
