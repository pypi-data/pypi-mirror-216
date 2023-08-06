// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { Image } from "react-invenio-forms";
import Overridable from "react-overridable";
import { Divider, Header, Message } from "semantic-ui-react";
import { toRelativeTime } from "react-invenio-forms";
import RequestStatus from "./RequestStatus";
import RequestTypeLabel from "./RequestTypeLabel";

const User = ({ user }) => (
  <div className="flex">
    <Image
      src={user.links.avatar}
      avatar
      size="tiny"
      className="mr-5"
      ui={false}
      rounded
    />
    <span>{user.profile?.full_name || user.username}</span>
  </div>
);
const Community = ({ community }) => (
  <div className="flex">
    <Image src={community.links.logo} avatar size="tiny" className="mr-5" ui={false} />
    <a href={`/communities/${community.slug}`}>{community.metadata.title}</a>
  </div>
);

const UserOrCommunity = ({ userData, details }) => {
  const isUser = "user" in userData;
  const isCommunity = "community" in userData;

  if (isUser) {
    return <User user={details} />;
  } else if (isCommunity) {
    return <Community community={details} />;
  }
};

const DeletedResource = ({ details }) => (
  <Message negative>{details.metadata.title}</Message>
);

class RequestMetadata extends Component {
  isResourceDeleted = (details) => details.is_ghost === true;

  render() {
    const { request } = this.props;
    const expandedCreatedBy = request.expanded?.created_by;
    const expandedReceiver = request.expanded?.receiver;
    return (
      <Overridable id="InvenioRequest.RequestMetadata.Layout" request={request}>
        <>
          <Header as="h3" size="tiny">
            {i18next.t("Creator")}
          </Header>
          {this.isResourceDeleted(expandedCreatedBy) ? (
            <DeletedResource details={expandedCreatedBy} />
          ) : (
            <UserOrCommunity
              userData={request.created_by}
              details={request.expanded?.created_by}
            />
          )}
          <Divider />

          <Header as="h3" size="tiny">
            {i18next.t("Receiver")}
          </Header>
          {this.isResourceDeleted(expandedReceiver) ? (
            <DeletedResource details={expandedReceiver} />
          ) : (
            <UserOrCommunity
              userData={request.receiver}
              details={request.expanded?.receiver}
            />
          )}
          <Divider />

          <Header as="h3" size="tiny">
            {i18next.t("Request type")}
          </Header>
          <RequestTypeLabel type={request.type} />
          <Divider />

          <Header as="h3" size="tiny">
            {i18next.t("Status")}
          </Header>
          <RequestStatus status={request.status} />
          <Divider />

          <Header as="h3" size="tiny">
            {i18next.t("Created")}
          </Header>
          {toRelativeTime(request.created, i18next.language)}

          {request.expires_at && (
            <>
              <Divider />
              <Header as="h3" size="tiny">
                {i18next.t("Expires")}
              </Header>
              {toRelativeTime(request.expires_at, i18next.language)}
            </>
          )}
          <Divider hidden />
        </>
      </Overridable>
    );
  }
}

RequestMetadata.propTypes = {
  request: PropTypes.object.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestMetadata",
  RequestMetadata
);
