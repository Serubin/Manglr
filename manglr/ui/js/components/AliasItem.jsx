
class AliasItem extends React.Component {

    deleteElement() {
        // requires prop.urlId
        // TODO ajax delete call
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
