import React from "react";
import "./PageAddProfile.css";
import { NotificationManager as nm } from "react-notifications";
import { getRequest, postRequest } from "../utils/request.jsx";
import FormLine from "./form/FormLine.jsx";
import Loading from "./box/Loading.jsx";
import { validateNotNull } from "../utils/re.jsx";

export default class PageAddProfile extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			first_name: "",
			last_name: "",
			telephone: "",
			domains_of_interest: null,
			experience: null,
			expertise_id: null,
			gender: null,
			how_heard: null,
			industry_id: null,
			mobile: "",
			nationality_id: null,
			profession_id: null,
			residency: null,
			sector: null,
			public: false,
			user_id: null,
			expertise: [],
			industries: [],
			countries: [],
			professions: [],
			domains: [],
			affiliated: false,
			agree_code: false,
			agree_privacy: false,
		};
	}

	componentDidMount() {
		getRequest.call(this, "public/get_public_countries", (data) => {
			this.setState({
				countries: data,
			});
		}, (error) => {
			nm.warning(error.message);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "public/get_public_professions", (data) => {
			this.setState({
				professions: data,
			});
		}, (error) => {
			nm.warning(error.message);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "public/get_public_industries", (data) => {
			this.setState({
				industries: data,
			});
		}, (error) => {
			nm.warning(error.message);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "public/get_public_domains", (data) => {
			this.setState({
				domains: data,
			});
		}, (error) => {
			nm.warning(error.message);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "public/get_public_expertise", (data) => {
			this.setState({
				expertise: data,
			});
		}, (error) => {
			nm.warning(error.message);
		}, (error) => {
			nm.error(error.message);
		});
	}

	changeState(field, value) {
		this.setState({ [field]: value });
	}

	isFormValid() {
		let valid = true;
		const malta = this.state.countries.find(
			(country) => (country.name === "Malta"),
		);
		console.log(malta);
		if (malta === undefined
			|| this.state.first_name === ""
			|| this.state.last_name === ""
			|| this.state.domains_of_interest === null
			|| this.state.experience === null
			|| this.state.expertise_id === null
			|| this.state.gender === null
			|| this.state.how_heard === null
			|| this.state.nationality_id === null
			|| this.state.profession_id === null
			|| this.state.residency === null
			|| (
				this.isStudentOrRetired() === false
				&& (this.state.sector === null || this.state.industry_id === null)
			)
		) {
			nm.warning("Please fill in all of the required fields");
			valid = false;
		}
		if (malta !== undefined) {
			if (
				this.state.nationality_id !== null
				&& this.state.residency !== ""
				&& this.state.nationality_id !== malta.id
				&& this.state.residency !== "Malta"
				&& this.state.residency !== "Gozo"
			) {
				nm.warning("The account is only available to Maltese or Gozo residents or Maltese nationals");
				valid = false;
			}
		}
		if (this.agreedToAll() !== true) {
			nm.warning("Please agree to all acknowledgements");
			valid = false;
		}
		return valid;
	}

	setRole(value) {
		this.changeState("profession_id", value);
		const role = this.state.professions.find(
			(p) => (p.id === value),
		);
		if (role !== undefined && (role.name === "Student" || role.name === "Retired")) {
			this.setState({ sector: null });
			this.setState({ industry_id: null });
		}
		this.forceUpdate();
	}

	isStudentOrRetired() {
		const role = this.state.professions.find(
			(p) => (p.id === this.state.profession_id),
		);
		if (role === undefined) {
			return false;
		}
		return role.name === "Student" || role.name === "Retired";
	}

	agreedToAll() {
		return this.state.agree_code && this.state.agree_privacy;
	}

	setDomains(name, value) {
		let domains = [];
		if (this.state.domains_of_interest !== null) {
			domains = this.state.domains_of_interest.split(" | ");
		}
		if (value === true && domains.includes(name) === false) {
			domains.push(name);
		}
		if (value === false && domains.includes(name) === true) {
			const index = domains.indexOf(name);
			console.log(index);
			if (index > -1) {
				domains.splice(index, 1);
			}
		}
		this.changeState("domains_of_interest", domains.length > 0 ? domains.join(" | ") : null);
	}

	submitCreationRequest() {
		if (this.isFormValid() === false) {
			return;
		}
		const params = {
			type: "NEW INDIVIDUAL ACCOUNT",
			request: "The user requests the creation of their profile",
			data: {
				first_name: this.state.first_name,
				last_name: this.state.last_name,
				telephone: this.state.telephone,
				domains_of_interest: this.state.domains_of_interest,
				experience: this.state.experience,
				expertise_id: this.state.expertise_id,
				gender: this.state.gender,
				how_heard: this.state.how_heard,
				industry_id: this.state.industry_id,
				mobile: this.state.mobile,
				nationality_id: this.state.nationality_id,
				profession_id: this.state.profession_id,
				residency: this.state.residency,
				sector: this.state.sector,
				public: this.state.public,
			},
		};
		postRequest.call(this, "private/add_request", params, () => {
			nm.info("The request has been sent and will be reviewed");
			this.fetchUser();
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	fetchUser() {
		getRequest.call(this, "private/get_my_user", (data) => {
			this.props.setUserStatus(data.status);
		}, (response2) => {
			nm.warning(response2.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	render() {
		return (
			<div id="PageAddProfile" className="page max-sized-page">
				<h1>Create your profile</h1>
				<div className="row">
					<div className="col-md-6">
						<FormLine
							label="Name *"
							fullWidth={true}
							value={this.state.first_name}
							onChange={(v) => this.changeState("first_name", v)}
							autofocus={true}
							onKeyDown={this.onKeyDown}
						/>
						<FormLine
							label="Surname *"
							fullWidth={true}
							value={this.state.last_name}
							onChange={(v) => this.changeState("last_name", v)}
							onKeyDown={this.onKeyDown}
						/>
						<FormLine
							label="Gender *"
							type="select"
							options={[
								{ value: null, label: "-" },
								{ value: "Male", label: "Male" },
								{ value: "Female", label: "Female" },
								{ value: "Non-binary", label: "Non-binary" },
								{ value: "Other", label: "Other" },
								{ value: "Prefer not to say", label: "Prefer not to say" },
							]}
							fullWidth={true}
							value={this.state.gender}
							onChange={(v) => this.changeState("gender", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="Telephone Number"
							fullWidth={true}
							value={this.state.telephone}
							onChange={(v) => this.changeState("telephone", v)}
							onKeyDown={this.onKeyDown}
						/>
						<FormLine
							label="Mobile Number"
							fullWidth={true}
							value={this.state.mobile}
							onChange={(v) => this.changeState("mobile", v)}
							onKeyDown={this.onKeyDown}
						/>
						<FormLine
							label="Role/Profession *"
							type="select"
							options={[{ value: null, label: "-" }].concat(
								this.state.professions.map((o) => ({
									label: (
										<>
											<div title={o.description}>{o.name}</div>
										</>
									),
									value: o.id,
								})),
							)}
							fullWidth={true}
							value={this.state.profession_id}
							onChange={(v) => this.setRole(v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="Sector *"
							type="select"
							options={[
								{ value: null, label: "-" },
								{ value: "Private", label: "Private" },
								{ value: "Public", label: "Public" },
							]}
							fullWidth={true}
							value={this.state.sector}
							onChange={(v) => this.changeState("sector", v)}
							onKeyDown={this.onKeyDown}
							disabled={this.isStudentOrRetired()}
							format={validateNotNull}
						/>
						<FormLine
							label="Industry *"
							type="select"
							options={[{ value: null, label: "-" }].concat(
								this.state.industries.map((o) => ({ label: o.name, value: o.id })),
							)}
							fullWidth={true}
							value={this.state.industry_id}
							onChange={(v) => this.changeState("industry_id", v)}
							onKeyDown={this.onKeyDown}
							disabled={this.isStudentOrRetired()}
							format={validateNotNull}
						/>
						<FormLine
							label="Nationality *"
							type="select"
							options={[{ value: null, label: "-" }].concat(
								this.state.countries.map((o) => ({ label: o.name, value: o.id })),
							)}
							fullWidth={true}
							value={this.state.nationality_id}
							onChange={(v) => this.changeState("nationality_id", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="Residency (Location) *"
							type="select"
							options={[
								{ value: null, label: "-" },
								{ value: "Malta", label: "Malta" },
								{ value: "Gozo", label: "Gozo" },
								{ value: "Outside of Malta", label: "Outside of Malta" },
							]}
							fullWidth={true}
							value={this.state.residency}
							onChange={(v) => this.changeState("residency", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="Years of professional experience in/related to cybersecurity *"
							type="select"
							options={[
								{ value: null, label: "-" },
								{ value: "Student", label: "Student" },
								{ value: "0 - 2", label: "0 - 2" },
								{ value: "2 - 5", label: "2 - 5" },
								{ value: "5 - 10", label: "5 - 10" },
								{ value: "10+", label: "10+" },
							]}
							fullWidth={true}
							value={this.state.experience}
							onChange={(v) => this.changeState("experience", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="Primary area of expertise in/related to cybersecurity *"
							type="select"
							options={[{ value: null, label: "-" }].concat(
								this.state.expertise.map((o) => ({
									label: (
										<>
											<div title={o.description}>{o.name}</div>
										</>
									),
									value: o.id,
								})),
							)}
							fullWidth={true}
							value={this.state.expertise_id}
							onChange={(v) => this.changeState("expertise_id", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
						<FormLine
							label="How did you hear about the Community *"
							type="select"
							options={[
								{ value: null, label: "-" },
								{ value: "Social Media", label: "Social Media" },
								{ value: "TV Advert", label: "TV Advert" },
								{ value: "Friend/Colleague", label: "Friend/Colleague" },
								{ value: "Government Website", label: "Government Website" },
								{ value: "European Commission", label: "European Commission" },
								{ value: "Other", label: "Other" },
							]}
							fullWidth={true}
							value={this.state.how_heard}
							onChange={(v) => this.changeState("how_heard", v)}
							onKeyDown={this.onKeyDown}
							format={validateNotNull}
						/>
					</div>
					<div className="col-md-6">
						<div className="FormLine-label font-weight-bold">Domains of interest *</div>
						{this.state.domains !== null
							? this.state.domains
								.map((c) => (
									<FormLine
										key={c.id}
										label={c.name}
										type={"checkbox"}
										value={false}
										onChange={(v) => this.setDomains(c.name, v)}
									/>
								))
							: <Loading
								height={200}
							/>
						}
						<hr />
						<div className="FormLine-label font-weight-bold">Privacy</div>
						<FormLine
							label={"Make my profile public"}
							type={"checkbox"}
							value={this.state.public}
							onChange={(v) => this.setState({ public: v })}
						/>
						<hr />
						<div className="FormLine-label font-weight-bold">Acknowledgements *</div>
						<div className={"FormLine"}>
							<div className="row">
								<div className="col-md-12">
									<div className={"FormLine-label"}>
										Please read and agree to the &nbsp;
										<a href='https://ncc-mita.gov.mt/community-code-of-conduct/'>Community&apos; s Code of Conduct</a> &amp;&nbsp;
										<a href='https://ncc-mita.gov.mt/privacy-policy/'>Privacy Policy and Terms of Use</a>.
									</div>
								</div>
							</div>
						</div>
						<FormLine
							label={"I acknowledge and agree to abide with the Community's Code of Conduct"}
							type={"checkbox"}
							value={this.state.agree_code}
							onChange={(v) => this.setState({ agree_code: v })}
						/>
						<FormLine
							label={"I acknowledge and agree with the Privacy Policy and Terms of Use"}
							type={"checkbox"}
							value={this.state.agree_privacy}
							onChange={(v) => this.setState({ agree_privacy: v })}
						/>
					</div>
				</div>

				<div className="row">
					<div className="col-md-12">
						<div className="right-buttons">
							<button
								className={"blue-background"}
								onClick={() => this.submitCreationRequest()}
							>
								Save my profile
							</button>
						</div>
					</div>
				</div>
			</div>

		);
	}
}
