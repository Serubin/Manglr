
class AliasItem extends React.Component {

    deleteElement() {

        $.ajax(API_BASE + "/urls/" + this.prop.urlId + "/alias/remove", {
            method: "POST",
            data: { "alias": this.prop.alias },
        });

    }

    render() {

        return (
            <li className="clearfix">
                <p className="pull-left">{this.props.alias}</p>
                <button type="button" className="btn btn-outline-danger pull-right" aria-label="Delete" onClick={this.deleteElement}>
                    Remove
                </button>
            </li>
        )
    }
}
