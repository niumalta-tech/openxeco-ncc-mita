import React from "react";
import "./UserEntity.css";
import Popup from "reactjs-popup";
import { NotificationManager as nm } from "react-notifications";
import Loading from "../../box/Loading.jsx";
import { validateEmail, validateTelephoneNumber } from "../../../utils/re.jsx";
import { getRequest, postRequest } from "../../../utils/request.jsx";
import FormLine from "../../button/FormLine.jsx";
import DialogConfirmation from "../../dialog/DialogConfirmation.jsx";

export default class UserEntity extends React.Component {
	constructor(props) {
		super(props);

		this.refresh = this.refresh.bind(this);
		this.getAllEntities = this.getAllEntities.bind(this);
		this.addUserEntity = this.addUserEntity.bind(this);
		this.deleteUserEntity = this.deleteUserEntity.bind(this);

		this.state = {
			email: "",
			telephone: "",
			level: "",
			userEntities: null,
			selectedEntity: null,
			selectedDepartment: null,
			allEntities: null,
			departments: null,
		};
	}

	componentDidMount() {
		this.refresh();
		this.getAllEntities();
	}

	refresh() {
		getRequest.call(this, "public/get_public_departments", (data) => {
			this.setState({
				departments: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "user/get_user_entities/" + this.props.id, (data) => {
			this.setState({
				userEntities: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	getAllEntities() {
		getRequest.call(this, "entity/get_entities", (data) => {
			this.setState({
				allEntities: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	addUserEntity(close) {
		const params = {
			user_id: this.props.id,
			entity_id: this.state.selectedEntity,
			department: this.state.selectedDepartment,
			work_email: this.state.email,
			seniority_level: this.state.level,
			work_telephone: this.state.telephone,
		};

		postRequest.call(this, "user/add_user_entity", params, () => {
			this.refresh();
			nm.info("The entity has been added to the user");
			close();
		}, (response) => {
			this.refresh();
			nm.warning(response.statusText);
		}, (error) => {
			this.refresh();
			nm.error(error.message);
		});
	}

	deleteUserEntity(id) {
		const params = {
			user_id: this.props.id,
			entity_id: id,
		};

		postRequest.call(this, "user/disassociate_user_entity", params, () => {
			this.refresh();
			nm.info("The user has been disassociated from the entity");
		}, (response) => {
			this.refresh();
			nm.warning(response.statusText);
		}, (error) => {
			this.refresh();
			nm.error(error.message);
		});
	}

	updateUserEntity(entity, department) {
		const params = {
			user: this.props.id,
			entity,
			department,
		};

		postRequest.call(this, "user/update_user_entity", params, () => {
			this.refresh();
			nm.info("The assignment has been updated");
		}, (response) => {
			this.refresh();
			nm.warning(response.statusText);
		}, (error) => {
			this.refresh();
			nm.error(error.message);
		});
	}

	formValid() {
		if (!validateEmail(this.state.email)
			|| (
				this.state.telephone !== ""
				&& !validateTelephoneNumber(this.state.telephone)
			)
			|| this.state.level === ""
			|| this.state.department === ""
			|| this.state.selectedEntity === null
		) {
			return false;
		}
		return true;
	}

	getEntityFromId(entityId) {
		if (this.state.allEntities) {
			const filteredEntities = this.state.allEntities.filter((c) => c.id === entityId);

			if (filteredEntities.length > 0) {
				return filteredEntities[0];
			}
			return null;
		}

		return null;
	}

	changeState(field, value) {
		this.setState({ [field]: value });
	}

	render() {
		return (
			<div className={"row"}>
				<div className="col-md-12">
					<div className={"top-right-buttons"}>
						<Popup
							className="Popup-full-size"
							trigger={
								<button
									className={"blue-background"}>
									<i className="fas fa-plus"/>
								</button>
							}
							modal
							closeOnDocumentClick
						>
							{(close) => <div className="row row-spaced">
								<div className="col-md-12">
									<h2>Associate user with entity</h2>

									<div className={"top-right-buttons"}>
										<button
											className={"grey-background"}
											data-hover="Close"
											data-active=""
											onClick={close}>
											<span><i className="far fa-times-circle"/></span>
										</button>
									</div>
								</div>
								<div className="col-md-12">
									{this.state.allEntities
										&& this.state.departments
										? <div>
											<FormLine
												label={"Entity"}
												type={"select"}
												value={this.state.selectedEntity}
												options={this.state.allEntities === null ? []
													: [{ value: null, label: "-" }].concat(
														this.state.allEntities.map((c) => ({ label: c.name, value: c.id })),
													)}
												onChange={(v) => this.setState({ selectedEntity: v })}
											/>
											<FormLine
												label="Work Email *"
												value={this.state.email}
												onChange={(v) => this.changeState("email", v)}
												autofocus={true}
												onKeyDown={this.onKeyDown}
											/>
											{!validateEmail(this.state.email) && this.state.email !== ""
												&& <div className="row">
													<div className="col-md-6"></div>
													<div className="col-md-6">
														<div className="validation-error">
															Please enter a valid email address
														</div>
													</div>
												</div>
											}
											<FormLine
												label="Work Telephone Number"
												value={this.state.telephone}
												onChange={(v) => this.changeState("telephone", v)}
												autofocus={true}
												onKeyDown={this.onKeyDown}
											/>
											{ !validateTelephoneNumber(this.state.telephone) && this.state.telephone !== ""
												&& <div className="row">
													<div className="col-md-6"></div>
													<div className="col-md-6">
														<div className="validation-error">
															Accepted Format: +1234567891, 1234567891
														</div>
													</div>
												</div>
											}
											<FormLine
												label={"Seniority Level *"}
												type={"select"}
												options={[
													{ value: "Board Member", label: "Board Member" },
													{ value: "Executive Management", label: "Executive Management" },
													{ value: "Senior Management", label: "Senior Management" },
													{ value: "Management", label: "Management" },
													{ value: "Senior", label: "Senior" },
													{ value: "Intermediate", label: "Intermediate" },
													{ value: "Entry-Level", label: "Entry-Level" },
												]}
												value={this.props.level}
												onChange={(v) => this.setState({ level: v })}
											/>
											<FormLine
												label={"Department"}
												type={"select"}
												value={this.state.selectedDepartment}
												options={this.state.departments === null
													? []
													: [{ value: null, label: "-" }].concat(
														this.state.departments.map((o) => ({ label: o.name, value: o.name })),
													)}
												onChange={(v) => this.setState({ selectedDepartment: v })}
											/>
											<div className="right-buttons">
												<button
													onClick={() => this.addUserEntity(close)}
													disabled={this.formValid() === false}>
													Add the assignment
												</button>
											</div>
										</div>
										: <Loading
											height={150}
										/>
									}
								</div>
							</div>}
						</Popup>
					</div>

					<h2>Associated entities</h2>
				</div>

				<div className="col-md-12">
					{this.state.userEntities
						? (this.state.userEntities.map((c) => (
							<div className={"row-spaced"} key={c.entity_id}>
								<h4>
									{this.getEntityFromId(c.entity_id)
										? this.getEntityFromId(c.entity_id).name
										: "Name not found"
									}
								</h4>

								<FormLine
									label={"Department"}
									type={"select"}
									options={this.state.departments
										? this.state.departments
											.map((d) => ({ label: d.name, value: d.name }))
										: []
									}
									value={c.department} // TODO
									onChange={(v) => this.updateUserEntity(c.entity_id, v)}
								/>

								<DialogConfirmation
									text={"Are you sure you want to delete this row?"}
									trigger={
										<button
											className={"red-background Table-right-button"}>
											<i className="fas fa-trash-alt"/> Disassociate
										</button>
									}
									afterConfirmation={() => this.deleteUserEntity(c.entity_id)}
								/>

							</div>
						)))
						: <Loading
							height={200}
						/>
					}
				</div>
			</div>
		);
	}
}
