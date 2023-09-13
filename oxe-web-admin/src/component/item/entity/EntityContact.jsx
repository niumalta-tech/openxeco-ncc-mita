import React from "react";
import "./EntityContact.css";
import { NotificationManager as nm } from "react-notifications";
import _ from "lodash";
import Loading from "../../box/Loading.jsx";
import Message from "../../box/Message.jsx";
import Contact from "../../button/Contact.jsx";
import { getRequest } from "../../../utils/request.jsx";

export default class EntityContact extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			contacts: [],
			entityName: props.name,
			contactEnums: null,
			users: [],
		};
	}

	componentDidMount() {
		if (!this.props.node) {
			this.refresh();
		}
	}

	refresh() {
		this.props.refresh();

		getRequest.call(this, "entity/get_entity_contacts/" + this.props.id, (data) => {
			if (Object.keys(data).length > 0) {
				this.setState({
					contacts: [data],
				});
			}
		}, () => {
			// nm.warning(response.statusText);
			this.setState({
				contacts: [],
			});
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "contact/get_contact_enums", (data) => {
			this.setState({
				contactEnums: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "entity/get_entity_users/" + this.props.id, (data) => {
			this.setState({
				users: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	addContact() {
		const contacts = _.cloneDeep(this.state.contacts);
		contacts.push({
			entity_id: this.props.id,
			user_id: null,
			type: "EMAIL ADDRESS",
			representative: "PHYSICAL PERSON",
			name: null,
			value: null,
		});

		this.setState({ contacts });
	}

	changeState(field, value) {
		this.setState({ [field]: value });
	}

	render() {
		if (this.props.node) {
			return <Message
				text={"Not applicable on remote entity"}
				height={300}
			/>;
		}

		if (this.state.contacts === null) {
			return <Loading height={300}/>;
		}

		return (
			<div className={"row"}>
				<div className="col-md-12">
					<h2>Contact</h2>
				</div>
				<div className="col-md-12">
					{this.state.contacts.length > 0
						? this.state.contacts.map((a) => (
							<Contact
								key={a.id}
								users={this.state.users}
								info={a}
								enums={this.state.contactEnums}
								afterAction={() => this.refresh()}
							/>
						))
						: <div className="text-center">
							<Message
								text={"No contact found on the database"}
								height={50}
							/>
							<button
								disabled={this.state.contacts.length > 0 || this.state.users.length < 1}
								className={"blue-background"}
								onClick={() => this.addContact()}>
								Add Contact <i className="fas fa-plus"/>
							</button>

							{this.state.users.length < 1
								&& <Message
									text={"Unable to add contact, no users associated with this entity"}
									height={50}
								/>
							}
						</div>
					}
				</div>
			</div>
		);
	}
}
