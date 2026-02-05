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
        ADD_METHOD_TO(TreeController::createNode, "{1}/nodes", Post);
        ADD_METHOD_TO(TreeController::getNode, "{1}/nodes/{2}", Get);
        ADD_METHOD_TO(TreeController::updateNode, "{1}/nodes/{2}", Put);
        ADD_METHOD_TO(TreeController::deleteNode, "{1}/nodes/{2}", Delete);

        // Metadata CRUD (single only, no bulk)
        ADD_METHOD_TO(TreeController::addMetadata, "{1}/nodes/{2}/metadata", Post);
        ADD_METHOD_TO(TreeController::updateMetadata, "{1}/metadata/{2}", Put);
        ADD_METHOD_TO(TreeController::deleteMetadata, "{1}/metadata/{2}", Delete);
    METHOD_LIST_END

    // Node CRUD
    void createNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb,
                    std::string connectionId);

    void getNode(const HttpRequestPtr &req,
                 std::function<void(const HttpResponsePtr &)> &&cb,
                 std::string connectionId,
                 int nodeId);

    void updateNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb,
                    std::string connectionId,
                    int nodeId);

    void deleteNode(const HttpRequestPtr &req,
                    std::function<void(const HttpResponsePtr &)> &&cb,
                    std::string connectionId,
                    int nodeId);

    // Metadata CRUD
    void addMetadata(const HttpRequestPtr &req,
                     std::function<void(const HttpResponsePtr &)> &&cb,
                     std::string connectionId,
                     int nodeId);

    void updateMetadata(const HttpRequestPtr &req,
                        std::function<void(const HttpResponsePtr &)> &&cb,
                        std::string connectionId,
                        int metadataId);

    void deleteMetadata(const HttpRequestPtr &req,
                        std::function<void(const HttpResponsePtr &)> &&cb,
                        std::string connectionId,
                        int metadataId);

private:
    std::pair<std::string, std::function<void(NodeMetadata &)>>
    detectValue(const Json::Value &value);
};
