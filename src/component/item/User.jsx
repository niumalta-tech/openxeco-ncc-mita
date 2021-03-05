import React, { Component } from "react";
import "./User.css";
import Popup from "reactjs-popup";
import { NotificationManager as nm } from "react-notifications";
import { getRequest, postRequest } from "../../utils/request";
import Loading from "../box/Loading";
import DialogConfirmation from "../dialog/DialogConfirmation";
import Tab from "../tab/Tab";
import UserGlobal from "./user/UserGlobal";
import UserCompany from "./user/UserCompany";

export default class User extends Component {
	constructor(props) {
		super(props);

		this.onClick = this.onClick.bind(this);
		this.onClose = this.onClose.bind(this);
		this.onOpen = this.onOpen.bind(this);
		this.confirmUserDeletion = this.confirmUserDeletion.bind(this);

		this.state = {
			isDetailOpened: false,
		};
	}

	onClick() {
		if (typeof this.props.disabled !== "undefined" || !this.props.disabled) {
			this.onOpen();

			const newState = !this.props.selected;
			if (typeof this.props.onClick !== "undefined") this.props.onClick(this.props.id, newState);
		}
	}

	onClose() {
		this.setState({ isDetailOpened: false }, () => {
			if (this.props.onClose !== undefined) this.props.onClose();
		});
	}

	onOpen() {
		this.setState({ isDetailOpened: true }, () => {
			if (this.props.onOpen !== undefined) this.props.onOpen();
		});
	}

	confirmUserDeletion() {
		const params = {
			id: this.props.id,
		};

		postRequest.call(this, "user/delete_user", params, (response) => {
			document.elementFromPoint(100, 0).click();
			nm.info("The user has been deleted");

			if (typeof this.props.afterDeletion !== "undefined") this.props.afterDeletion();
		}, (response) => {
			this.refreshUserData();
			nm.warning(response.statusText);
		}, (error) => {
			this.refreshUserData();
			nm.error(error.message);
		});
	}

	render() {
		return (
			<Popup
				className="Popup-full-size"
				trigger={
					<div className={"User"}>
						<i className="fas fa-user"/>
						<div className={"User-name"}>
							{this.props.email}
						</div>
					</div>
				}
				modal
				closeOnDocumentClick
				onClose={this.onClose}
				onOpen={this.onOpen}
			>
				<div className="row">
					<div className="col-md-12">
						<div className={"top-right-buttons"}>
							<DialogConfirmation
								text={"Are you sure you want to delete this user?"}
								trigger={
									<button
										className={"red-background"}
										onClick={() => this.deleteUser()}>
										<i className="fas fa-trash-alt"/>
									</button>
								}
								afterConfirmation={() => this.confirmUserDeletion()}
							/>
						</div>
						<h1 className="User-title">
							{this.props.email}
						</h1>

						<Tab
							menu={["Global", "Company"]}
							content={[
								<UserGlobal
									id={this.props.id}
								/>,
								<UserCompany
									id={this.props.id}
									name={this.props.name}
								/>,
							]}
						/>
					</div>
				</div>
			</Popup>
		);
	}
}
